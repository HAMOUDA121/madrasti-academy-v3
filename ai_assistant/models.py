from django.db import models
from django.contrib.auth.models import User

class ChatHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    subject = models.CharField(max_length=50, default='عام')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.subject} ({self.created_at.strftime('%Y-%m-%d')})"
