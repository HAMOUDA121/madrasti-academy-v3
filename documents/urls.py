from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DocumentViewSet, UploadDocumentView

router = DefaultRouter()
router.register(r'list', DocumentViewSet)

urlpatterns = [
    path('upload/', UploadDocumentView.as_view(), name='upload_document'),
    path('', include(router.urls)),
]
