from django.urls import path
from .views import CreateOrderView, UpdateOrderStatusView

urlpatterns = [
    path('orders/', CreateOrderView.as_view(), name='create_order'),
    path('orders/<int:order_id>/status/', UpdateOrderStatusView.as_view(), name='update_order_status'),
]
