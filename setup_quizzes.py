import os

# 1. إنشاء مجلد التطبيق
os.makedirs('quizzes', exist_ok=True)

# 2. ملف النماذج Models
models_py = """from django.db import models

class Quiz(models.Model):
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=100)
    xp_reward = models.PositiveIntegerField(default=50)

    def __str__(self):
        return f"{self.title} ({self.subject})"

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return f"{self.quiz.title} - {self.text[:30]}"

class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=250)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text
"""
with open('quizzes/models.py', 'w', encoding='utf-8') as f:
    f.write(models_py)

# 3. ملف الإدارة Admin
admin_py = """from django.contrib import admin
from .models import Quiz, Question, Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]

admin.site.register(Quiz)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
"""
with open('quizzes/admin.py', 'w', encoding='utf-8') as f:
    f.write(admin_py)

# 4. ملفات REST API
serializers_py = """from rest_framework import serializers
from .models import Quiz, Question, Choice

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'text']

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)
    class Meta:
        model = Question
        fields = ['id', 'text', 'choices']

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'subject', 'xp_reward', 'questions']
"""
with open('quizzes/serializers.py', 'w', encoding='utf-8') as f:
    f.write(serializers_py)

views_py = """from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from gamification.models import StudentProfile
from .models import Quiz, Question, Choice
from .serializers import QuizSerializer

class QuizViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

@method_decorator(csrf_exempt, name='dispatch')
class SubmitQuizView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, quiz_id):
        answers = request.data.get('answers', {})
        try:
            quiz = Quiz.objects.get(id=quiz_id)
        except Quiz.DoesNotExist:
            return Response({'error': 'الاختبار غير موجود'}, status=status.HTTP_404_NOT_FOUND)

        correct_count = 0
        total_questions = quiz.questions.count()

        for q in quiz.questions.all():
            selected_choice_id = answers.get(str(q.id))
            if selected_choice_id:
                if Choice.objects.filter(id=selected_choice_id, question=q, is_correct=True).exists():
                    correct_count += 1

        score_pct = int((correct_count / total_questions) * 100) if total_questions > 0 else 0
        xp_earned = 0

        profile = StudentProfile.objects.first()
        if score_pct >= 50 and profile:
            xp_earned = quiz.xp_reward
            profile.add_xp(xp_earned)

        return Response({
            'score_pct': score_pct,
            'correct_count': correct_count,
            'total_questions': total_questions,
            'xp_earned': xp_earned,
            'new_total_xp': profile.xp_points if profile else 0,
            'new_level': profile.level if profile else 1
        })
"""
with open('quizzes/views.py', 'w', encoding='utf-8') as f:
    f.write(views_py)

urls_py = """from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuizViewSet, SubmitQuizView

router = DefaultRouter()
router.register(r'', QuizViewSet)

urlpatterns = [
    path('submit/<int:quiz_id>/', SubmitQuizView.as_view(), name='submit_quiz'),
    path('', include(router.urls)),
]
"""
with open('quizzes/urls.py', 'w', encoding='utf-8') as f:
    f.write(urls_py)

with open('quizzes/__init__.py', 'w') as f:
    f.write('')

# 5. تحديث settings.py
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
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
"""
with open('config/settings.py', 'w', encoding='utf-8') as f:
    f.write(settings_py)

# 6. تحديث URLs الرئيسة
config_urls = """from django.contrib import admin
from django.urls import path, include
from .views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/gamification/', include('gamification.urls')),
    path('api/ai/', include('ai_assistant.urls')),
    path('api/quizzes/', include('quizzes.urls')),
    path('', home_view, name='home'),
]
"""
with open('config/urls.py', 'w', encoding='utf-8') as f:
    f.write(config_urls)

# 7. تحديث الواجهة الرئيسية لتضمين الكويز التفاعلي
index_html = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>لوحة الطالب | مدرستي أكاديمي V3</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-900 text-slate-100 min-h-screen font-sans">
    
    <!-- Navbar -->
    <nav class="border-b border-slate-800 bg-slate-950/80 backdrop-blur sticky top-0 z-50 px-6 py-4 flex justify-between items-center">
        <div class="flex items-center gap-3">
            <span class="text-3xl">🎓</span>
            <div>
                <h1 class="text-lg font-bold bg-gradient-to-r from-blue-400 to-indigo-400 bg-clip-text text-transparent">
                    مدرستي أكاديمي V3
                </h1>
                <p class="text-xs text-slate-400">المنظومة التعليمية التونسية 🇹🇳</p>
            </div>
        </div>
        <div class="flex items-center gap-4">
            <span id="streak-badge" class="bg-amber-500/10 border border-amber-500/30 text-amber-400 px-3 py-1.5 rounded-xl text-xs font-semibold flex items-center gap-2">
                🔥 <span id="streak-count">0</span> أيام متتالية
            </span>
            <a href="/admin/" class="bg-indigo-600 hover:bg-indigo-500 text-white px-4 py-2 rounded-xl text-xs font-semibold transition">
                لوحة الإدارة
            </a>
        </div>
    </nav>

    <main class="max-w-7xl mx-auto p-6 md:p-8 space-y-8">
        
        <!-- Student Profile Card -->
        <div class="bg-gradient-to-r from-indigo-950/60 to-slate-900 border border-indigo-500/30 rounded-2xl p-6 md:p-8 shadow-xl">
            <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
                <div class="space-y-2">
                    <div class="inline-block bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 px-3 py-1 rounded-full text-xs font-medium" id="student-grade">
                        جاري التحميل...
                    </div>
                    <h2 class="text-2xl md:text-3xl font-bold text-white flex items-center gap-3">
                        <span id="student-name">...</span>
                        <span class="bg-emerald-500/20 text-emerald-400 text-xs px-2.5 py-1 rounded-lg border border-emerald-500/30">نشط</span>
                    </h2>
                    <p class="text-slate-400 text-sm">مباشر من قاعدة بيانات Django REST Framework</p>
                </div>

                <div class="flex items-center gap-6 bg-slate-900/80 border border-slate-800 p-4 rounded-xl w-full md:w-auto justify-around">
                    <div class="text-center">
                        <p class="text-xs text-slate-400 mb-1">المستوى</p>
                        <p id="student-level" class="text-3xl font-extrabold text-indigo-400">1</p>
                    </div>
                    <div class="h-8 w-[1px] bg-slate-800"></div>
                    <div class="text-center">
                        <p class="text-xs text-slate-400 mb-1">مجموع الـ XP</p>
                        <p id="student-xp" class="text-3xl font-extrabold text-amber-400">0</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Section: Interactive Quizzes -->
        <div class="bg-slate-800/50 border border-slate-700/80 rounded-2xl p-6 space-y-4 shadow-xl">
            <div class="flex items-center justify-between border-b border-slate-700/60 pb-4">
                <div class="flex items-center gap-3">
                    <span class="text-3xl">📝</span>
                    <div>
                        <h3 class="font-bold text-lg text-white">التمارين والكويزات التفاعلية</h3>
                        <p class="text-xs text-slate-400">اختبر معلوماتك في امتحانات الباكالوريا واكسب نقاط XP ممتازة!</p>
                    </div>
                </div>
            </div>

            <div id="quiz-container" class="space-y-4">
                <p class="text-sm text-slate-400">جاري تحميل الاختبارات...</p>
            </div>
        </div>

        <!-- Section: AI Smart Tutor Chat Box -->
        <div class="bg-slate-800/50 border border-slate-700/80 rounded-2xl p-6 space-y-4 shadow-xl">
            <div class="flex items-center justify-between border-b border-slate-700/60 pb-4">
                <div class="flex items-center gap-3">
                    <span class="text-3xl">🤖</span>
                    <div>
                        <h3 class="font-bold text-lg text-white">المعلم الذكي (RAG AI Assistant)</h3>
                        <p class="text-xs text-slate-400">اسأل في الرياضيات، الفيزياء أو المناهج التونسية واحصل على +10 XP!</p>
                    </div>
                </div>
            </div>

            <div id="chat-box" class="bg-slate-950/70 border border-slate-800 rounded-xl p-4 h-48 overflow-y-auto text-sm space-y-3">
                <div class="bg-slate-800/80 p-3 rounded-lg text-slate-300 max-w-xl">
                    👋 أهلاً بك! أنا مساعدك التعليمي التونسي. تفضل بطرح سؤالك للبدء بالمراجعة.
                </div>
            </div>

            <div class="flex gap-3">
                <input type="text" id="ai-question" placeholder="اكتب سؤالك هنا..." class="flex-grow bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-indigo-500 text-white">
                <button onclick="askAI()" class="bg-indigo-600 hover:bg-indigo-500 text-white px-6 py-3 rounded-xl font-bold text-sm transition shadow-lg shadow-indigo-600/30">
                    إرسال
                </button>
            </div>
        </div>

        <!-- Badges Section -->
        <div>
            <h3 class="text-xl font-bold text-white mb-4 flex items-center gap-2">
                <span>🏆</span> الشارات والأوسمة المستحقة
            </h3>
            <div id="badges-container" class="grid grid-cols-1 md:grid-cols-3 gap-4"></div>
        </div>

    </main>

    <script>
        let currentQuizId = null;

        async function loadProfileData() {
            try {
                const resProfiles = await fetch('/api/gamification/profiles/');
                const profiles = await resProfiles.json();
                if (profiles && profiles.length > 0) {
                    const student = profiles[0];
                    document.getElementById('student-name').innerText = student.username;
                    document.getElementById('student-grade').innerText = student.grade_display;
                    document.getElementById('student-level').innerText = student.level;
                    document.getElementById('student-xp').innerText = student.xp_points + ' XP';
                    document.getElementById('streak-count').innerText = student.streak_days;
                }

                const resBadges = await fetch('/api/gamification/badges/');
                const badges = await resBadges.json();
                const container = document.getElementById('badges-container');
                container.innerHTML = '';
                badges.forEach(b => {
                    container.innerHTML += `
                        <div class="bg-slate-800/60 border border-slate-700/60 rounded-xl p-5 flex items-start gap-4">
                            <div class="text-3xl bg-slate-900 p-3 rounded-xl border border-slate-800">${b.icon}</div>
                            <div>
                                <h4 class="font-bold text-white text-base">${b.title}</h4>
                                <p class="text-xs text-slate-400 my-1">${b.description}</p>
                                <span class="inline-block bg-amber-500/10 text-amber-400 text-[10px] px-2 py-0.5 rounded font-semibold border border-amber-500/20">
                                    تتطلب: ${b.xp_required} XP
                                </span>
                            </div>
                        </div>
                    `;
                });

                loadQuizzes();
            } catch (err) {
                console.error(err);
            }
        }

        async function loadQuizzes() {
            const res = await fetch('/api/quizzes/');
            const quizzes = await res.json();
            const container = document.getElementById('quiz-container');
            if(quizzes.length === 0) {
                container.innerHTML = '<p class="text-xs text-slate-400">لا توجد اختبارات متاحة حالياً.</p>';
                return;
            }

            const q = quizzes[0];
            currentQuizId = q.id;
            let html = `
                <div class="bg-slate-900/80 p-5 rounded-xl border border-slate-700 space-y-4">
                    <div class="flex justify-between items-center border-b border-slate-800 pb-3">
                        <h4 class="font-bold text-indigo-300 text-base">${q.title} (${q.subject})</h4>
                        <span class="bg-amber-500/10 text-amber-400 border border-amber-500/30 text-xs px-3 py-1 rounded-full font-semibold">+${q.xp_reward} XP عند الإنجاز</span>
                    </div>
                    <form id="quiz-form" class="space-y-4">
            `;

            q.questions.forEach((qItem, idx) => {
                html += `
                    <div class="space-y-2">
                        <p class="text-sm font-semibold text-white">${idx + 1}. ${qItem.text}</p>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-2">
                `;
                qItem.choices.forEach(c => {
                    html += `
                        <label class="flex items-center gap-2 bg-slate-800/80 p-2.5 rounded-lg border border-slate-700/60 hover:border-indigo-500 cursor-pointer text-xs">
                            <input type="radio" name="q_${qItem.id}" value="${c.id}" class="accent-indigo-500">
                            <span>${c.text}</span>
                        </label>
                    `;
                });
                html += `</div></div>`;
            });

            html += `
                    </form>
                    <div class="flex justify-between items-center pt-2">
                        <button onclick="submitQuiz()" class="bg-emerald-600 hover:bg-emerald-500 text-white px-6 py-2.5 rounded-xl text-xs font-bold transition">
                            تسليم الإجابات
                        </button>
                        <span id="quiz-result" class="text-sm font-bold"></span>
                    </div>
                </div>
            `;
            container.innerHTML = html;
        }

        async function submitQuiz() {
            if(!currentQuizId) return;
            const form = document.getElementById('quiz-form');
            const formData = new FormData(form);
            const answers = {};

            for(let [key, val] of formData.entries()) {
                const qId = key.replace('q_', '');
                answers[qId] = parseInt(val);
            }

            const res = await fetch(`/api/quizzes/submit/${currentQuizId}/`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({answers: answers})
            });

            const data = await res.json();
            const resultSpan = document.getElementById('quiz-result');

            if(data.score_pct >= 50) {
                resultSpan.className = 'text-emerald-400 text-sm font-bold';
                resultSpan.innerText = `🎉 ممتاز! النتيجة: ${data.score_pct}% (${data.correct_count}/${data.total_questions}) - حصلت على +${data.xp_earned} XP!`;
                document.getElementById('student-xp').innerText = data.new_total_xp + ' XP';
                document.getElementById('student-level').innerText = data.new_level;
            } else {
                resultSpan.className = 'text-amber-400 text-sm font-bold';
                resultSpan.innerText = `النتيجة: ${data.score_pct}% (${data.correct_count}/${data.total_questions}) - حاول مجدداً لتحقيق 50% أو أكثر والحصول على الـ XP!`;
            }
        }

        async function askAI() {
            const input = document.getElementById('ai-question');
            const q = input.value.trim();
            if(!q) return;

            const chatBox = document.getElementById('chat-box');
            chatBox.innerHTML += `<div class="bg-indigo-900/50 border border-indigo-500/30 p-3 rounded-lg text-indigo-100 max-w-xl ml-auto text-right">${q}</div>`;
            input.value = '';

            try {
                const res = await fetch('/api/ai/chat/', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({question: q})
                });
                const data = await res.json();
                if (data.answer) {
                    chatBox.innerHTML += `<div class="bg-slate-800/80 p-3 rounded-lg text-slate-200 max-w-xl">🤖 ${data.answer} <span class="text-amber-400 text-xs block mt-1">+${data.xp_earned} XP 🏆</span></div>`;
                    document.getElementById('student-xp').innerText = data.new_total_xp + ' XP';
                    document.getElementById('student-level').innerText = data.new_level;
                }
                chatBox.scrollTop = chatBox.scrollHeight;
            } catch (err) {
                chatBox.innerHTML += `<div class="text-red-400 p-2 text-xs">حدث خطأ أثناء الاتصال.</div>`;
            }
        }

        document.addEventListener('DOMContentLoaded', loadProfileData);
    </script>
</body>
</html>
"""
with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(index_html)

print("تم بناء نظام التمارين والكويزات بنجاح!")
