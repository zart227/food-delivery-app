from django.urls import path
from .views import UserProfileView, UpdateNotificationPreferencesView

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('profile/notifications/', UpdateNotificationPreferencesView.as_view(), name='update-notifications'),
] 