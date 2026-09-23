import os

views_py = """import os
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
            return Response({'error': 'يرجى كتابة سؤال'}, status=status.HTTP_400_BAD_REQUEST)

        # إعداد النظام وتوجيه النموذج نحو المنهج التونسي
        system_instruction = (
            "أنت معلم ذكي خبير في المناهج التعليمية التونسية (خاصة الباكالوريا والنوفيام). "
            "أجب باللغة العربية بطريقة مبسطة، مشجعة، وواضحة، مع تقديم خطوات الحل التوضيحية في الرياضيات والفيزياء."
        )

        ai_response_text = ""

        if GEMINI_API_KEY:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
                payload = {
                    "contents": [{
                        "parts": [{"text": f"{system_instruction}\n\nسؤال الطالب: {user_question}"}]
                    }]
                }
                res = requests.post(url, json=payload, timeout=10)
                data = res.json()
                ai_response_text = data['candidates'][0]['content']['parts'][0]['text']
            except Exception as e:
                ai_response_text = f"إجابة تجريبية (لم يتم الاتصال بـ Gemini API): إجابة مفصلة عن '{user_question}'"
        else:
            ai_response_text = f"🤖 [وضع المعاينة]: شكراً لسؤالك حول '{user_question}'. للحصول على إجابات مباشرة من Gemini، قم بإضافة GEMINI_API_KEY."

        # إضافة XP للطالب
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
    f.write(views_py)

print("تم تحديث وحدة المعلم الذكي بنجاح!")
