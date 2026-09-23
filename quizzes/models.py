from django.db import models

class Quiz(models.Model):
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=100)
    xp_reward = models.PositiveIntegerField(default=50)

    def __str__(self):
        return f"{self.title} ({self.subject})"

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return f"{self.quiz.title} - {self.text[:30]}"

class Choice(models.Model):
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=250)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text
