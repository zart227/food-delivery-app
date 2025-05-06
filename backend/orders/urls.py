from django.urls import path
from .views import CreateOrderView, UpdateOrderStatusView, ListOrdersView

urlpatterns = [
    path('orders/', ListOrdersView.as_view(), name='orders-list'),
    path('orders/create/', CreateOrderView.as_view(), name='create_order'),
    path('orders/<int:order_id>/status/', UpdateOrderStatusView.as_view(), name='update_order_status'),
]
