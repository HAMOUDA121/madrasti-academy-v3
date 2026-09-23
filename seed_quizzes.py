import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from quizzes.models import Quiz, Question, Choice

quiz, _ = Quiz.objects.get_or_create(
    title="اختبار تجريبي: رياضيات الباكالوريا (الأعداد المركبة)",
    subject="رياضيات",
    defaults={'xp_reward': 50}
)

# السؤال الأول
q1, _ = Question.objects.get_or_create(
    quiz=quiz,
    text="ما هو مرافق العدد المركب z = 3 + 4i ؟"
)
Choice.objects.get_or_create(question=q1, text="3 - 4i", defaults={'is_correct': True})
Choice.objects.get_or_create(question=q1, text="-3 + 4i", defaults={'is_correct': False})
Choice.objects.get_or_create(question=q1, text="-3 - 4i", defaults={'is_correct': False})

# السؤال الثاني
q2, _ = Question.objects.get_or_create(
    quiz=quiz,
    text="معيار العدد المركب z = 3 + 4i يساوي:"
)
Choice.objects.get_or_create(question=q2, text="5", defaults={'is_correct': True})
Choice.objects.get_or_create(question=q2, text="7", defaults={'is_correct': False})
Choice.objects.get_or_create(question=q2, text="25", defaults={'is_correct': False})

print("تم تعبئة اختبار الرياضيات بنجاح!")
