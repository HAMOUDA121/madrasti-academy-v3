from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

TUNISIAN_GRADES = [
    ('7_BASIC', '7ème Année Base (7 أساسي)'),
    ('8_BASIC', '8ème Année Base (8 أساسي)'),
    ('9_BASIC', '9ème Année Base (9 أساسي - النوفيام)'),
    ('1_SEC', '1ère Année Secondaire (1 ثانوي)'),
    ('2_SEC', '2ème Année Secondaire (2 ثانوي)'),
    ('3_SEC', '3ème Année Secondaire (3 ثانوي)'),
    ('BAC', 'Baccalauréat (الباكالوريا)'),
]

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    grade_level = models.CharField(max_length=20, choices=TUNISIAN_GRADES, default='BAC')
    xp_points = models.PositiveIntegerField(default=0)
    level = models.PositiveIntegerField(default=1)
    streak_days = models.PositiveIntegerField(default=0)
    last_activity = models.DateField(default=timezone.now)

    def add_xp(self, points):
        self.xp_points += points
        self.level = (self.xp_points // 500) + 1
        self.save()

    def __str__(self):
        return f"{self.user.username} - المستوى {self.level} ({self.get_grade_level_display()})"

class Badge(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=10, default="🏆")
    xp_required = models.PositiveIntegerField(default=100)

    def __str__(self):
        return f"{self.icon} {self.title}"

class StudentBadge(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'badge')
