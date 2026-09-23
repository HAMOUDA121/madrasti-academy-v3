from rest_framework import viewsets
from .models import StudentProfile, Badge
from .serializers import StudentProfileSerializer, BadgeSerializer

class StudentProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer

class BadgeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer
