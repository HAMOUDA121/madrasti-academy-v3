from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def parent_dashboard(request):
    return render(request, 'parent_dashboard.html')

@login_required
def teacher_dashboard(request):
    return render(request, 'teacher_dashboard.html')

@login_required
def achievements(request):
    return render(request, 'achievements.html')

@login_required
def ai_tutor(request):
    return render(request, 'ai_tutor.html')
