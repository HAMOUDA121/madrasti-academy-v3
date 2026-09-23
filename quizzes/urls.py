from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuizViewSet, SubmitQuizView

router = DefaultRouter()
router.register(r'', QuizViewSet)

urlpatterns = [
    path('submit/<int:quiz_id>/', SubmitQuizView.as_view(), name='submit_quiz'),
    path('', include(router.urls)),
]
