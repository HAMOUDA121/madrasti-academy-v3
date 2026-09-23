import os

# 1. ????? ???? accounts
os.makedirs('accounts', exist_ok=True)

with open('accounts/__init__.py', 'w') as f:
    f.write('')

# 2. ??? ??????? Models
models_py = """from django.db import models
# ?????? ????? User ????????? ????? ?? Django ?? ???? ?? StudentProfile
"""
with open('accounts/models.py', 'w', encoding='utf-8') as f:
    f.write(models_py)

# 3. ??? Views ????????
views_py = """from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from gamification.models import StudentProfile

@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        username = request.data.get('username', '').strip()
        password = request.data.get('password', '').strip()
        grade = request.data.get('grade', 'BAC_MATH')

        if not username or not password:
            return Response({'error': '??? ???????? ????? ???? ???????'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': '??? ???????? ?????? ??????'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password)
        profile, created = StudentProfile.objects.get_or_create(user=user, defaults={'grade': grade})
        login(request, user)

        return Response({
            'message': '?? ????? ?????? ?????? ?????? ?????!',
            'username': user.username,
            'grade': profile.get_grade_display(),
            'xp_points': profile.xp_points,
            'level': profile.level
        }, status=status.HTTP_201_CREATED)

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        username = request.data.get('username', '').strip()
        password = request.data.get('password', '').strip()

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            profile, _ = StudentProfile.objects.get_or_create(user=user)
            return Response({
                'message': '?? ????? ?????? ?????',
                'username': user.username,
                'grade': profile.get_grade_display(),
                'xp_points': profile.xp_points,
                'level': profile.level
            })
        return Response({'error': '??? ???????? ?? ???? ???? ??? ?????'}, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        logout(request)
        return Response({'message': '?? ????? ?????? ?????'})

class CurrentUserView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'authenticated': False})

        profile, _ = StudentProfile.objects.get_or_create(user=request.user)
        return Response({
            'authenticated': True,
            'username': request.user.username,
            'grade': profile.get_grade_display(),
            'xp_points': profile.xp_points,
            'level': profile.level,
            'streak_days': profile.streak_days
        })
"""
with open('accounts/views.py', 'w', encoding='utf-8') as f:
    f.write(views_py)

# 4. ??? URLs ????????
urls_py = """from django.urls import path
from .views import RegisterView, LoginView, LogoutView, CurrentUserView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/', CurrentUserView.as_view(), name='current_user'),
]
"""
with open('accounts/urls.py', 'w', encoding='utf-8') as f:
    f.write(urls_py)

# 5. ????? ai_assistant/views.py ???? ?????? ????????? ??????
ai_views_py = """import os
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from gamification.models import StudentProfile

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

@method_decorator(csrf_exempt, name='dispatch')
class AIChatView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        user_question = request.data.get('question', '')
        if not user_question:
            return Response({'error': '???? ????? ????'}, status=status.HTTP_400_BAD_REQUEST)

        system_instruction = (
            "??? ???? ??? ???? ?? ??????? ????????? ???????? (???? ??????????? ?????????). "
            "??? ?????? ??????? ?????? ?????? ?????? ??????? ?? ????? ????? ???? ????????? ?? ????????? ?????????."
        )

        ai_response_text = ""

        if GEMINI_API_KEY:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
                prompt_text = system_instruction + "\\n\\n???? ??????: " + user_question
                payload = {
                    "contents": [{
                        "parts": [{"text": prompt_text}]
                    }]
                }
                res = requests.post(url, json=payload, timeout=10)
                data = res.json()
                ai_response_text = data['candidates'][0]['content']['parts'][0]['text']
            except Exception as e:
                ai_response_text = f"????? ??????? (?? ??? ??????? ?? Gemini API): ????? ????? ?? '{user_question}'"
        else:
            ai_response_text = f"?? [??? ????????]: ????? ?????? ??? '{user_question}'. ?????? ??? ?????? ?????? ?? Gemini? ?? ?????? GEMINI_API_KEY."

        # ??? ?????? ????????? ?????? ?????? ?? ?????? ????? ?????????
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

# 6. ????? settings.py ?????? accounts
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

# 7. ????? config/urls.py
config_urls = """from django.contrib import admin
from django.urls import path, include
from .views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/gamification/', include('gamification.urls')),
    path('api/ai/', include('ai_assistant.urls')),
    path('api/quizzes/', include('quizzes.urls')),
    path('api/payments/', include('payments.urls')),
    path('', home_view, name='home'),
]
"""
with open('config/urls.py', 'w', encoding='utf-8') as f:
    f.write(config_urls)

print("?? ???? ???? ???????? ???????? ?????? ????????? ?????!")
