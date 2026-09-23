import os

# 1. إنشاء مجلد التطبيق
os.makedirs('ai_assistant', exist_ok=True)

# 2. إنشاء نماذج البيانات للمحادثة
models_py = """from django.db import models
from django.contrib.auth.models import User

class ChatHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    subject = models.CharField(max_length=50, default='عام')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.subject} ({self.created_at.strftime('%Y-%m-%d')})"
"""
with open('ai_assistant/models.py', 'w', encoding='utf-8') as f:
    f.write(models_py)

# 3. إعداد الـ View المساعد للـ RAG AI
views_py = """from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from gamification.models import StudentProfile
from .models import ChatHistory

class AIChatView(APIView):
    def post(self, request):
        question = request.data.get('question', '').strip()
        if not question:
            return Response({'error': 'يرجى تقديم سؤال محدد'}, status=status.HTTP_400_BAD_REQUEST)

        # استجابة ذكية محاكاة للمنهج التونسي
        answer = f"بناءً على المنهج التونسي: بالإجابة على سؤالك '{question}'، نوصي بالمراجعة بالاعتماد على التمارين المحلولة والتركيز على القواعد الأساسية في امتحانات الباكالوريا."
        if "رياضيات" in question or "math" in question.lower():
            answer = "في مادة الرياضيات (المنهج التونسي): تذكر دائماً التحقق من مجال التعريف (Domaine de définition) ودراسة الاستمرارية والاشتقاق قبل رسم المنحنى البياني."
        elif "فيزياء" in question or "physique" in question.lower():
            answer = "في مادة الفيزياء: تذكر تطبيق قانون نيوتن الثاني وقوانين الدارات الكهربائية RLC بدقة مع كتابة الوحدات حسب النظام الدولي."

        # إضافة 10 نقاط XP للطالب كمكافأة للتعلم
        profile = StudentProfile.objects.first()
        if profile:
            profile.add_xp(10)

        # حفظ السجل
        if profile:
            ChatHistory.objects.create(user=profile.user, question=question, answer=answer)

        return Response({
            'question': question,
            'answer': answer,
            'xp_earned': 10,
            'new_total_xp': profile.xp_points if profile else 0,
            'new_level': profile.level if profile else 1
        })
"""
with open('ai_assistant/views.py', 'w', encoding='utf-8') as f:
    f.write(views_py)

urls_py = """from django.urls import path
from .views import AIChatView

urlpatterns = [
    path('chat/', AIChatView.as_view(), name='ai_chat'),
]
"""
with open('ai_assistant/urls.py', 'w', encoding='utf-8') as f:
    f.write(urls_py)

with open('ai_assistant/__init__.py', 'w') as f:
    f.write('')

# 4. تحديث settings.py لإضافة التطبيق الجديد
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

# 5. تحديث config/urls.py
config_urls = """from django.contrib import admin
from django.urls import path, include
from .views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/gamification/', include('gamification.urls')),
    path('api/ai/', include('ai_assistant.urls')),
    path('', home_view, name='home'),
]
"""
with open('config/urls.py', 'w', encoding='utf-8') as f:
    f.write(config_urls)

# 6. إضافة نافذة المحادثة التفاعلية في الواجهة الأمامية
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

            <!-- Chat Output Box -->
            <div id="chat-box" class="bg-slate-950/70 border border-slate-800 rounded-xl p-4 h-48 overflow-y-auto text-sm space-y-3">
                <div class="bg-slate-800/80 p-3 rounded-lg text-slate-300 max-w-xl">
                    👋 أهلاً بك! أنا مساعدك التعليمي التونسي. تفضل بطرح سؤالك للبدء بالمراجعة.
                </div>
            </div>

            <!-- Chat Input Form -->
            <div class="flex gap-3">
                <input type="text" id="ai-question" placeholder="اكتب سؤالك هنا (مثال: كيف أستعد لاختبار الرياضيات؟)..." class="flex-grow bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-indigo-500 text-white">
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
            } catch (err) {
                console.error(err);
            }
        }

        async function askAI() {
            const input = document.getElementById('ai-question');
            const q = input.value.trim();
            if(!q) return;

            const chatBox = document.getElementById('chat-box');
            chatBox.innerHTML += `<div class="bg-indigo-900/50 border border-indigo-500/30 p-3 rounded-lg text-indigo-100 max-w-xl mr-auto text-left">${q}</div>`;
            input.value = '';

            try {
                const res = await fetch('/api/ai/chat/', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({question: q})
                });
                const data = await res.json();
                chatBox.innerHTML += `<div class="bg-slate-800/80 p-3 rounded-lg text-slate-200 max-w-xl">🤖 ${data.answer} <span class="text-amber-400 text-xs block mt-1">+${data.xp_earned} XP 🏆</span></div>`;
                chatBox.scrollTop = chatBox.scrollHeight;

                // تحديث النقاط لحظياً في أعلى الصفحة
                document.getElementById('student-xp').innerText = data.new_total_xp + ' XP';
                document.getElementById('student-level').innerText = data.new_level;
            } catch (err) {
                chatBox.innerHTML += `<div class="text-red-400 p-2 text-xs">حدث خطأ أثناء التواصل مع المعلم الذكي.</div>`;
            }
        }

        document.addEventListener('DOMContentLoaded', loadProfileData);
    </script>
</body>
</html>
"""
with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(index_html)

print("تم تفعيل المعلم الذكي وتجهيز واجهة الشات والمكافآت!")
