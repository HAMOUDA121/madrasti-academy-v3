from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentProfileViewSet, BadgeViewSet

router = DefaultRouter()
router.register(r'profiles', StudentProfileViewSet)
router.register(r'badges', BadgeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
