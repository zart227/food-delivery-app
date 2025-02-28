from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import UserProfileSerializer
from django.core.files.storage import default_storage
import os

# Create your views here.

class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Представление для просмотра и обновления профиля пользователя.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        # Обработка загрузки аватара
        avatar_file = request.FILES.get('avatar')
        if avatar_file:
            # Удаляем старый аватар, если он существует
            if instance.avatar:
                if os.path.isfile(instance.avatar.path):
                    default_storage.delete(instance.avatar.path)
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


class UpdateNotificationPreferencesView(APIView):
    """
    Представление для обновления настроек уведомлений пользователя.
    """
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = request.user
        preferences = request.data.get('preferences', {})
        
        # Обновляем настройки уведомлений
        user.notification_preferences.update(preferences)
        user.save()
        
        return Response({
            'status': 'success',
            'notification_preferences': user.notification_preferences
        })
