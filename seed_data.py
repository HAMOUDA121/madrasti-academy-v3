import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from gamification.models import Badge, StudentProfile
from django.contrib.auth.models import User

# 1. إنشاء أوسمة افتراضية
badges = [
    {"title": "بطل الباكالوريا", "description": "أنهى أول 10 تمارين بنجاح", "icon": "🎓", "xp_required": 100},
    {"title": "المواظب التونسي", "description": "سجل حضور يومي لمدة 7 أيام متتالية", "icon": "🔥", "xp_required": 250},
    {"title": "عبقري الرياضيات", "description": "حصل على العلامة الكاملة في اختبار تجريبي", "icon": "📐", "xp_required": 500},
]

for b in badges:
    Badge.objects.get_or_create(title=b["title"], defaults=b)

# 2. إنشاء حساب تجريبي وتوصيله بالبروفايل
user, created = User.objects.get_or_create(username="student_tn", email="student@madrasti.tn")
if created:
    user.set_password("madrasti123")
    user.save()

profile, _ = StudentProfile.objects.get_or_create(user=user, defaults={'grade_level': 'BAC', 'xp_points': 650, 'level': 2, 'streak_days': 5})
print("تمت إضافة الأوسمة والبروفايل التجريبي بنجاح!")
