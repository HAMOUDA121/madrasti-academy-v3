import os

os.makedirs('templates', exist_ok=True)

index_html = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>مدرستي أكاديمي V3 | MADRASTI Academy</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-900 text-white min-h-screen font-sans">
    <nav class="border-b border-slate-800 bg-slate-950/50 backdrop-blur px-6 py-4 flex justify-between items-center">
        <div class="flex items-center gap-3">
            <span class="text-2xl">🎓</span>
            <h1 class="text-xl font-bold bg-gradient-to-r from-blue-400 to-indigo-500 bg-clip-text text-transparent">
                مدرستي أكاديمي V3 Ultimate
            </h1>
        </div>
        <span class="bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 px-3 py-1 rounded-full text-xs font-semibold">
            المنظومة التونسية 🇹🇳
        </span>
    </nav>

    <main class="max-w-6xl mx-auto p-6 md:p-10">
        <div class="bg-gradient-to-br from-indigo-900/40 to-slate-800/40 border border-indigo-500/20 rounded-2xl p-8 mb-10 text-center shadow-2xl">
            <h2 class="text-3xl md:text-4xl font-extrabold mb-4">مرحباً بك في بيئة التطوير المتكاملة</h2>
            <p class="text-slate-400 max-w-2xl mx-auto text-sm md:text-base mb-6">
                تم تشغيل الخادم بنجاح. البيئة مجهزة بكامل التقنيات: Django 4.2، REST API، ونظام التلعيب والمكافآت.
            </p>
            <div class="flex flex-wrap justify-center gap-4">
                <a href="/admin/" class="bg-indigo-600 hover:bg-indigo-500 text-white px-6 py-2.5 rounded-xl font-semibold transition shadow-lg shadow-indigo-600/30">
                    لوحة التحكم (Admin)
                </a>
            </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div class="bg-slate-800/50 border border-slate-700/50 rounded-xl p-6">
                <div class="text-3xl mb-3">🏆</div>
                <h3 class="font-bold text-lg mb-2">نظام التلعيب (Gamification)</h3>
                <p class="text-xs text-slate-400">حساب نقاط XP، الأوسمة، وسلسلة الحضور اليومي للطلاب.</p>
            </div>
            <div class="bg-slate-800/50 border border-slate-700/50 rounded-xl p-6">
                <div class="text-3xl mb-3">🤖</div>
                <h3 class="font-bold text-lg mb-2">المعلم الذكي (RAG AI)</h3>
                <p class="text-xs text-slate-400">مساعد إلكتروني مربوط بالبرامج والمناهج التعليمية التونسية.</p>
            </div>
            <div class="bg-slate-800/50 border border-slate-700/50 rounded-xl p-6">
                <div class="text-3xl mb-3">💳</div>
                <h3 class="font-bold text-lg mb-2">الدفع المحلي (Flouci)</h3>
                <p class="text-xs text-slate-400">بوابة دفع مدمجة لااشتراكات المحتوى المتميز بالدينار التونسي.</p>
            </div>
        </div>
    </main>
</body>
</html>"""

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(index_html)

views_py = """from django.shortcuts import render

def home_view(request):
    return render(request, 'index.html')
"""
with open('config/views.py', 'w', encoding='utf-8') as f:
    f.write(views_py)

urls_py = """from django.contrib import admin
from django.urls import path
from .views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
]
"""
with open('config/urls.py', 'w', encoding='utf-8') as f:
    f.write(urls_py)

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

print("تم تجهيز الواجهة والإعدادات بنجاح!")
