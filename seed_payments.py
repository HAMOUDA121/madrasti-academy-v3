import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from payments.models import SubscriptionPlan

plans = [
    {"name": "عرض الباكالوريا الشامل", "description": "وصول كامل للتمارين المحلولة وشرح المعلم الذكي مع متابعة يومية", "price_tnd": 29.000, "duration_days": 30},
    {"name": "اشتراك الثلاثي الأول (نوفيام/باك)", "description": "تغطية كاملة لبرنامج الثلاثي الأول + كويزات غير محدودة", "price_tnd": 69.000, "duration_days": 90},
]

for p in plans:
    SubscriptionPlan.objects.get_or_create(name=p["name"], defaults=p)

print("تمت إضافة خطط اشتراك Flouci بنجاح!")
