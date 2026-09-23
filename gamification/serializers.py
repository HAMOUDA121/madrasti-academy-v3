from rest_framework import serializers
from .models import StudentProfile, Badge, StudentBadge

class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = '__all__'

class StudentProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    grade_display = serializers.CharField(source='get_grade_level_display', read_only=True)

    class Meta:
        model = StudentProfile
        fields = ['id', 'username', 'grade_level', 'grade_display', 'xp_points', 'level', 'streak_days', 'last_activity']
