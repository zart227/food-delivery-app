from django.contrib import admin
from django.db.models import Sum, Count
from django.utils.html import format_html
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('get_total_price',)
    
    def get_total_price(self, obj):
        return obj.price * obj.quantity if obj else 0
    get_total_price.short_description = 'Общая стоимость'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_price', 'created_at', 'colored_status')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'delivery_address')
    readonly_fields = ('total_price',)
    inlines = [OrderItemInline]
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Информация о заказе', {
            'fields': ('user', 'status', 'total_price')
        }),
        ('Доставка', {
            'fields': ('delivery_address', 'delivery_notes')
        }),
    )

    def colored_status(self, obj):
        colors = {
            'pending': 'orange',
            'processing': 'blue',
            'shipping': 'purple',
            'delivered': 'green',
            'cancelled': 'red'
        }
        return format_html(
            '<span style="color: {};">{}</span>',
            colors.get(obj.status, 'black'),
            obj.get_status_display()
        )
    colored_status.short_description = 'Статус'

    def changelist_view(self, request, extra_context=None):
        # Добавляем статистику
        extra_context = extra_context or {}
        
        # Общая статистика
        total_orders = Order.objects.count()
        total_revenue = Order.objects.aggregate(total=Sum('total_price'))['total'] or 0
        
        # Статистика по статусам
        status_stats = Order.objects.values('status').annotate(
            count=Count('id')
        ).order_by('status')
        
        # Статистика по дням
        daily_stats = Order.objects.extra(
            select={'day': 'date(created_at)'}
        ).values('day').annotate(
            count=Count('id'),
            revenue=Sum('total_price')
        ).order_by('-day')[:7]

        extra_context.update({
            'total_orders': total_orders,
            'total_revenue': total_revenue,
            'status_stats': status_stats,
            'daily_stats': daily_stats,
        })
        
        return super().changelist_view(request, extra_context=extra_context)

    class Media:
        css = {
            'all': ['admin/css/custom_admin.css']
        }
