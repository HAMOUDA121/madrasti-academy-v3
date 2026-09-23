from django.shortcuts import render

def parent_dashboard(request):
    return render(request, 'parent_dashboard.html')

def teacher_dashboard(request):
    return render(request, 'teacher_dashboard.html')

def achievements(request):
    return render(request, 'achievements.html')

def ai_tutor(request):
    return render(request, 'ai_tutor.html')
