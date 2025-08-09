from django.urls import path
from . import views

app_name = 'avatar_processor'

urlpatterns = [
    # Main avatar processing endpoint
    path('process-avatar/', views.AvatarProcessAPIView.as_view(), name='process_avatar'),
    
    # Status and monitoring endpoints
    path('avatar-status/<int:avatar_id>/', views.avatar_status, name='avatar_status'),
    path('health/', views.health_check, name='health_check'),
    path('info/', views.api_info, name='api_info'),
]
