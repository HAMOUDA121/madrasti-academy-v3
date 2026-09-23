from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from gamification.models import StudentProfile

@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        username = request.data.get('username', '').strip()
        password = request.data.get('password', '').strip()
        grade = request.data.get('grade', 'BAC_MATH')

        if not username or not password:
            return Response({'error': 'اسم المستخدم وكلمة السر مطلوبان'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'اسم المستخدم مستخدم بالفعل'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password)
        profile, created = StudentProfile.objects.get_or_create(user=user, defaults={'grade': grade})
        login(request, user)

        return Response({
            'message': 'تم إنشاء الحساب وتسجيل الدخول بنجاح!',
            'username': user.username,
            'grade': profile.get_grade_display(),
            'xp_points': profile.xp_points,
            'level': profile.level
        }, status=status.HTTP_201_CREATED)

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        username = request.data.get('username', '').strip()
        password = request.data.get('password', '').strip()

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            profile, _ = StudentProfile.objects.get_or_create(user=user)
            return Response({
                'message': 'تم تسجيل الدخول بنجاح',
                'username': user.username,
                'grade': profile.get_grade_display(),
                'xp_points': profile.xp_points,
                'level': profile.level
            })
        return Response({'error': 'اسم المستخدم أو كلمة السر غير صحيحة'}, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        logout(request)
        return Response({'message': 'تم تسجيل الخروج بنجاح'})

class CurrentUserView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'authenticated': False})

        profile, _ = StudentProfile.objects.get_or_create(user=request.user)
        return Response({
            'authenticated': True,
            'username': request.user.username,
            'grade': profile.get_grade_display(),
            'xp_points': profile.xp_points,
            'level': profile.level,
            'streak_days': profile.streak_days
        })
