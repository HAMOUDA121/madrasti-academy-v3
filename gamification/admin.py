from django.contrib import admin
from .models import StudentProfile, Badge, StudentBadge

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'grade_level', 'xp_points', 'level', 'streak_days', 'last_activity')
    list_filter = ('grade_level', 'level')
    search_fields = ('user__username', 'user__email')

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ('icon', 'title', 'xp_required')

@admin.register(StudentBadge)
class StudentBadgeAdmin(admin.ModelAdmin):
    list_display = ('student', 'badge', 'earned_at')
