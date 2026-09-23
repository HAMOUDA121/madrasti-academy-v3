import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.apps import apps

def seed_all():
    print("==> Starting Data Seeding Process...")

    # 1. Feed Subscription Plans (Payments)
    if apps.is_installed('payments'):
        SubscriptionPlan = apps.get_model('payments', 'SubscriptionPlan')
        plans = [
            {'name': 'الخطة المجانية', 'price': 0, 'description': 'وصول محدود للمحتوى والمساعد الذكي'},
            {'name': 'اشتراط المراجعة النهائية', 'price': 29.99, 'description': 'فتح جميع الدروس والملخصات والاختبارات التفاعلية'},
            {'name': 'الاشتراك الشامل + AI', 'price': 49.99, 'description': 'وصول كامل بدون حدود + مساعد الذكاء الاصطناعي RAG'}
        ]
        for plan in plans:
            SubscriptionPlan.objects.get_or_create(name=plan['name'], defaults=plan)
        print("  [✓] Subscription Plans created.")

    # 2. Feed Gamification Badges
    if apps.is_installed('gamification'):
        Badge = apps.get_model('gamification', 'Badge')
        badges = [
            {'name': 'المستكشف', 'description': 'عند إكمال أول درس في المنصة'},
            {'name': 'بطل الاختبارات', 'description': 'عند الحصول على العلامة الكاملة في اختبار'},
            {'name': 'المستمر', 'description': 'الدخول للمنصة لمدة 7 أيام متتالية'}
        ]
        for badge in badges:
            Badge.objects.get_or_create(name=badge['name'], defaults=badge)
        print("  [✓] Badges created.")

    # 3. Feed Documents / Courses
    if apps.is_installed('documents'):
        Document = apps.get_model('documents', 'Document')
        docs = [
            {'title': 'مقدمة في الرياضيات - البكالوريا', 'content': 'ملخص الشامل لدرس الدوال والتكامل.'},
            {'title': 'مراجعة الفيزياء - الفيزياء الحديثة', 'content': 'شرح مفاهيم الطاقة والكهرباء التفاعلية.'}
        ]
        for doc in docs:
            Document.objects.get_or_create(title=doc['title'], defaults=doc)
        print("  [✓] Sample Documents created.")

    # 4. Feed Quizzes and Questions
    if apps.is_installed('quizzes'):
        Quiz = apps.get_model('quizzes', 'Quiz')
        Question = apps.get_model('quizzes', 'Question')
        Choice = apps.get_model('quizzes', 'Choice')

        quiz, created = Quiz.objects.get_or_create(title='اختبار الرياضيات التجريبي 01')
        if created:
            q1 = Question.objects.create(quiz=quiz, text='ما هو مشتق الدالة f(x) = x² ؟')
            Choice.objects.create(question=q1, text='2x', is_correct=True)
            Choice.objects.create(question=q1, text='x', is_correct=False)
            Choice.objects.create(question=q1, text='2', is_correct=False)

        print("  [✓] Sample Quizzes and Questions created.")

    print("==> ALL DATA SEEDED SUCCESSFULLY!")

if __name__ == '__main__':
    try:
        seed_all()
    except Exception as e:
        print(f"==> WARNING during seeding: {e}")