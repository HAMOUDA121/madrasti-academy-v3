from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubscriptionPlanViewSet, CreateFlouciPaymentView, VerifyPaymentView

router = DefaultRouter()
router.register(r'plans', SubscriptionPlanViewSet)

urlpatterns = [
    path('create/', CreateFlouciPaymentView.as_view(), name='create_flouci_payment'),
    path('verify/', VerifyPaymentView.as_view(), name='verify_flouci_payment'),
    path('', include(router.urls)),
]
