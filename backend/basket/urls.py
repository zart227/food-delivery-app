from django.urls import path
from .views import BasketView

urlpatterns = [
    path('basket/', BasketView.as_view(), name='basket'),
    path('basket/<int:pk>/', BasketView.as_view(), name='basket-item'),
]
