from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/gamification/', include('gamification.urls')),
    path('api/ai/', include('ai_assistant.urls')),
    path('api/quizzes/', include('quizzes.urls')),
    path('api/payments/', include('payments.urls')),
    path('api/documents/', include('documents.urls')),
    path('', home_view, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
