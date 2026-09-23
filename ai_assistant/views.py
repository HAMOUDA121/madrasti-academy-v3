import os
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from gamification.models import StudentProfile
from documents.models import DocumentChunk

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

@method_decorator(csrf_exempt, name='dispatch')
class AIChatView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        user_question = request.data.get('question', '')
        if not user_question:
            return Response({'error': 'يرجى كتابة سؤال'}, status=status.HTTP_400_BAD_REQUEST)

        # RAG Engine: البحث عن الأجزاء الأكثر مطابقة للسؤال من المناهج المرفوعة
        words = [w for w in user_question.split() if len(w) > 2]
        relevant_chunks = []
        
        if words:
            from django.db.models import Q
            query = Q()
            for w in words:
                query |= Q(content__icontains=w)
            matching_chunks = DocumentChunk.objects.filter(query)[:3]
            for c in matching_chunks:
                relevant_chunks.append(f"[{c.document.title} - {c.document.get_grade_display()}]: {c.content}")

        context_str = ""
        if relevant_chunks:
            context_str = "\n\nالمراجع المعتمدة من المناهج والامتحانات المرفوعة:\n" + "\n---\n".join(relevant_chunks)

        system_instruction = (
            "أنت معلم ذكي خبير في المناهج التعليمية التونسية (خاصة الباكالوريا والنوفيام). "
            "أجب باللغة العربية بطريقة مبسطة وواضحة مع الخطوات التوضيحية. "
            "إذا توفرت مراجع من المناهج المرفوعة، اعتمد عليها ووافي الطالب بالمصدر."
        )

        ai_response_text = ""

        if GEMINI_API_KEY:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
                prompt_text = system_instruction + context_str + "\n\nسؤال الطالب: " + user_question
                payload = {
                    "contents": [{
                        "parts": [{"text": prompt_text}]
                    }]
                }
                res = requests.post(url, json=payload, timeout=12)
                data = res.json()
                ai_response_text = data['candidates'][0]['content']['parts'][0]['text']
            except Exception as e:
                ai_response_text = f"إجابة تجريبية مع سياق المناهج: إجابة مفصلة عن '{user_question}'"
        else:
            ai_response_text = f"🤖 [RAG Enabled]: شكراً لسؤالك حول '{user_question}'."
            if context_str:
                ai_response_text += f" تم استخراج السياق التالي من المناهج:\n{context_str}"

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
