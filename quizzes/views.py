from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from gamification.models import StudentProfile
from .models import Quiz, Question, Choice
from .serializers import QuizSerializer

class QuizViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

@method_decorator(csrf_exempt, name='dispatch')
class SubmitQuizView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, quiz_id):
        answers = request.data.get('answers', {})
        try:
            quiz = Quiz.objects.get(id=quiz_id)
        except Quiz.DoesNotExist:
            return Response({'error': 'الاختبار غير موجود'}, status=status.HTTP_404_NOT_FOUND)

        correct_count = 0
        total_questions = quiz.questions.count()

        for q in quiz.questions.all():
            selected_choice_id = answers.get(str(q.id))
            if selected_choice_id:
                if Choice.objects.filter(id=selected_choice_id, question=q, is_correct=True).exists():
                    correct_count += 1

        score_pct = int((correct_count / total_questions) * 100) if total_questions > 0 else 0
        xp_earned = 0

        profile = StudentProfile.objects.first()
        if score_pct >= 50 and profile:
            xp_earned = quiz.xp_reward
            profile.add_xp(xp_earned)

        return Response({
            'score_pct': score_pct,
            'correct_count': correct_count,
            'total_questions': total_questions,
            'xp_earned': xp_earned,
            'new_total_xp': profile.xp_points if profile else 0,
            'new_level': profile.level if profile else 1
        })
