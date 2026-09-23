import os

# 1. ????? ???? ??????? ????????? ????????
os.makedirs('gamification', exist_ok=True)

# 2. ??? ??????? (Models)
models_py = """from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

TUNISIAN_GRADES = [
    ('7_BASIC', '7ème Année Base (7 ?????)'),
    ('8_BASIC', '8ème Année Base (8 ?????)'),
    ('9_BASIC', '9ème Année Base (9 ????? - ????????)'),
    ('1_SEC', '1ère Année Secondaire (1 ?????)'),
    ('2_SEC', '2ème Année Secondaire (2 ?????)'),
    ('3_SEC', '3ème Année Secondaire (3 ?????)'),
    ('BAC', 'Baccalauréat (???????????)'),
]

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    grade_level = models.CharField(max_length=20, choices=TUNISIAN_GRADES, default='BAC')
    xp_points = models.PositiveIntegerField(default=0)
    level = models.PositiveIntegerField(default=1)
    streak_days = models.PositiveIntegerField(default=0)
    last_activity = models.DateField(default=timezone.now)

    def add_xp(self, points):
        self.xp_points += points
        self.level = (self.xp_points // 500) + 1
        self.save()

    def __str__(self):
        return f"{self.user.username} - ??????? {self.level} ({self.get_grade_level_display()})"

class Badge(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=10, default="??")
    xp_required = models.PositiveIntegerField(default=100)

    def __str__(self):
        return f"{self.icon} {self.title}"

class StudentBadge(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'badge')
"""
with open('gamification/models.py', 'w', encoding='utf-8') as f:
    f.write(models_py)

# 3. ??? ??????? (Admin)
admin_py = """from django.contrib import admin
from .models import StudentProfile, Badge, StudentBadge

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'grade_level', 'xp_points', 'level', 'streak_days', 'last_activity')
    list_filter = ('grade_level', 'level')
    search_fields = ('user__username', 'user__email')

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('icon', 'title', 'xp_required')

@admin.register(StudentBadge)
class StudentBadgeAdmin(admin.ModelAdmin):
    list_display = ('student', 'badge', 'earned_at')
"""
with open('gamification/admin.py', 'w', encoding='utf-8') as f:
    f.write(admin_py)

# 4. ????? REST API (Serializers & Views)
serializers_py = """from rest_framework import serializers
from .models import StudentProfile, Badge, StudentBadge

class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = '__all__'

class StudentProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    grade_display = serializers.CharField(source='get_grade_level_display', read_only=True)

    class Meta:
        model = StudentProfile
        fields = ['id', 'username', 'grade_level', 'grade_display', 'xp_points', 'level', 'streak_days', 'last_activity']
"""
with open('gamification/serializers.py', 'w', encoding='utf-8') as f:
    f.write(serializers_py)

views_py = """from rest_framework import viewsets
from .models import StudentProfile, Badge
from .serializers import StudentProfileSerializer, BadgeSerializer

class StudentProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer

class BadgeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer
"""
with open('gamification/views.py', 'w', encoding='utf-8') as f:
    f.write(views_py)

urls_py = """from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentProfileViewSet, BadgeViewSet

router = DefaultRouter()
router.register(r'profiles', StudentProfileViewSet)
router.register(r'badges', BadgeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
"""
with open('gamification/urls.py', 'w', encoding='utf-8') as f:
    f.write(urls_py)

# 5. ????? settings.py
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

# 6. ????? config/urls.py ??? API
config_urls = """from django.contrib import admin
from django.urls import path, include
from .views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/gamification/', include('gamification.urls')),
    path('', home_view, name='home'),
]
"""
with open('config/urls.py', 'w', encoding='utf-8') as f:
    f.write(config_urls)

with open('gamification/__init__.py', 'w') as f:
    f.write('')

print("?? ????? ???? ??????? ???????? ??????? ?????!")
