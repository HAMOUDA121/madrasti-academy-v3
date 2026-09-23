import os

# 1. إنشاء مجلد التطبيق
os.makedirs('documents', exist_ok=True)
os.makedirs('media/documents', exist_ok=True)

with open('documents/__init__.py', 'w') as f:
    f.write('')

# 2. ملف النماذج Models
models_py = """from django.db import models

class Document(models.Model):
    GRADE_CHOICES = [
        ('BAC_MATH', 'باكالوريا رياضيات'),
        ('BAC_INFO', 'باكالوريا علوم الإعلامية'),
        ('BAC_SC', 'باكالوريا علوم تجريبية'),
        ('9TH_GRADE', 'التاسعة أساسي (نوفيام)'),
    ]
    title = models.CharField(max_length=200)
    grade = models.CharField(max_length=20, choices=GRADE_CHOICES, default='BAC_MATH')
    subject = models.CharField(max_length=100, default='عام')
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.get_grade_display()})"

class DocumentChunk(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='chunks')
    content = models.TextField()
    chunk_index = models.IntegerField()

    def __str__(self):
        return f"{self.document.title} - جزء {self.chunk_index}"
"""
with open('documents/models.py', 'w', encoding='utf-8') as f:
    f.write(models_py)

# 3. ملف الإدارة Admin
admin_py = """from django.contrib import admin
from .models import Document, DocumentChunk

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'grade', 'subject', 'uploaded_at')

@admin.register(DocumentChunk)
class DocumentChunkAdmin(admin.ModelAdmin):
    list_display = ('document', 'chunk_index')
"""
with open('documents/admin.py', 'w', encoding='utf-8') as f:
    f.write(admin_py)

# 4. ملف Serializers و Views للوثائق
serializers_py = """from rest_framework import serializers
from .models import Document, DocumentChunk

class DocumentSerializer(serializers.ModelSerializer):
    grade_display = serializers.CharField(source='get_grade_display', read_only=False)

    class Meta:
        model = Document
        fields = ['id', 'title', 'grade', 'grade_display', 'subject', 'file', 'uploaded_at']
"""
with open('documents/serializers.py', 'w', encoding='utf-8') as f:
    f.write(serializers_py)

views_py = """import pypdf
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import Document, DocumentChunk
from .serializers import DocumentSerializer

class DocumentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Document.objects.all().order_by('-uploaded_at')
    serializer_class = DocumentSerializer

@method_decorator(csrf_exempt, name='dispatch')
class UploadDocumentView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        title = request.data.get('title')
        grade = request.data.get('grade', 'BAC_MATH')
        subject = request.data.get('subject', 'عام')
        file_obj = request.FILES.get('file')

        if not title or not file_obj:
            return Response({'error': 'يرجى تقديم العنوان والملف'}, status=status.HTTP_400_BAD_REQUEST)

        doc = Document.objects.create(
            title=title,
            grade=grade,
            subject=subject,
            file=file_obj
        )

        # استخراج النصوص وتقسيمها إلى Chunks لتقنية RAG
        try:
            reader = pypdf.PdfReader(doc.file.path)
            full_text = ""
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\\n"

            # تقسيم النص إلى فقرات بحجم ~600 حرف
            chunk_size = 600
            chunks = [full_text[i:i+chunk_size] for i in range(0, len(full_text), chunk_size)]
            
            for idx, c in enumerate(chunks):
                if c.strip():
                    DocumentChunk.objects.create(
                        document=doc,
                        content=c.strip(),
                        chunk_index=idx
                    )

            return Response({
                'message': f'تم رفع الوثيقة بنجاح وتم توليد {len(chunks)} جزءاً للمواضيع والمناهج!',
                'document': DocumentSerializer(doc).data
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': f'فشل استخراج النص من PDF: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
"""
with open('documents/views.py', 'w', encoding='utf-8') as f:
    f.write(views_py)

urls_py = """from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DocumentViewSet, UploadDocumentView

router = DefaultRouter()
router.register(r'list', DocumentViewSet)

urlpatterns = [
    path('upload/', UploadDocumentView.as_view(), name='upload_document'),
    path('', include(router.urls)),
]
"""
with open('documents/urls.py', 'w', encoding='utf-8') as f:
    f.write(urls_py)

# 5. تحديث المعلم الذكي RAG AI Assistant في ai_assistant/views.py
ai_views_py = """import os
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from gamification.models import StudentProfile
from documents.models import DocumentChunk

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

@method_decorator(csrf_exempt, name='dispatch')
class AIChatView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        user_question = request.data.get('question', '')
        if not user_question:
            return Response({'error': 'يرجى كتابة سؤال'}, status=status.HTTP_400_BAD_REQUEST)

        # RAG Engine: البحث عن الأجزاء الأكثر مطابقة للسؤال من المناهج المرفوعة
        words = [w for w in user_question.split() if len(w) > 2]
        relevant_chunks = []
        
        if words:
            from django.db.models import Q
            query = Q()
            for w in words:
                query |= Q(content__icontains=w)
            matching_chunks = DocumentChunk.objects.filter(query)[:3]
            for c in matching_chunks:
                relevant_chunks.append(f"[{c.document.title} - {c.document.get_grade_display()}]: {c.content}")

        context_str = ""
        if relevant_chunks:
            context_str = "\\n\\nالمراجع المعتمدة من المناهج والامتحانات المرفوعة:\\n" + "\\n---\\n".join(relevant_chunks)

        system_instruction = (
            "أنت معلم ذكي خبير في المناهج التعليمية التونسية (خاصة الباكالوريا والنوفيام). "
            "أجب باللغة العربية بطريقة مبسطة وواضحة مع الخطوات التوضيحية. "
            "إذا توفرت مراجع من المناهج المرفوعة، اعتمد عليها ووافي الطالب بالمصدر."
        )

        ai_response_text = ""

        if GEMINI_API_KEY:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
                prompt_text = system_instruction + context_str + "\\n\\nسؤال الطالب: " + user_question
                payload = {
                    "contents": [{
                        "parts": [{"text": prompt_text}]
                    }]
                }
                res = requests.post(url, json=payload, timeout=12)
                data = res.json()
                ai_response_text = data['candidates'][0]['content']['parts'][0]['text']
            except Exception as e:
                ai_response_text = f"إجابة تجريبية مع سياق المناهج: إجابة مفصلة عن '{user_question}'"
        else:
            ai_response_text = f"🤖 [RAG Enabled]: شكراً لسؤالك حول '{user_question}'."
            if context_str:
                ai_response_text += f" تم استخراج السياق التالي من المناهج:\\n{context_str}"

        if request.user.is_authenticated:
            profile, _ = StudentProfile.objects.get_or_create(user=request.user)
        else:
            profile = StudentProfile.objects.first()

        xp_earned = 10
        if profile:
            profile.add_xp(xp_earned)

        return Response({
            'answer': ai_response_text,
            'xp_earned': xp_earned,
            'new_total_xp': profile.xp_points if profile else 0,
            'new_level': profile.level if profile else 1
        })
"""
with open('ai_assistant/views.py', 'w', encoding='utf-8') as f:
    f.write(ai_views_py)

# 6. تحديث settings.py لإضافة documents و MEDIA
settings_py = """import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'secret-key-123'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'gamification',
    'ai_assistant',
    'quizzes',
    'payments',
    'accounts',
    'documents',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_URL = 'static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
"""
with open('config/settings.py', 'w', encoding='utf-8') as f:
    f.write(settings_py)

# 7. تحديث config/urls.py لدعم الروابط والـ Media
config_urls = """from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/gamification/', include('gamification.urls')),
    path('api/ai/', include('ai_assistant.urls')),
    path('api/quizzes/', include('quizzes.urls')),
    path('api/payments/', include('payments.urls')),
    path('api/documents/', include('documents.urls')),
    path('', home_view, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"""
with open('config/urls.py', 'w', encoding='utf-8') as f:
    f.write(config_urls)

print("تم إنشاء تطبيق RAG الوثائق وتحديث الإعدادات بنجاح!")
