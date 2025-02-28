from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description', 'product_count')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Количество продуктов'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'is_available', 'is_vegetarian', 'is_spicy', 'display_image')
    list_filter = ('category', 'is_available', 'is_vegetarian', 'is_spicy')
    search_fields = ('title', 'description')
    list_editable = ('is_available', 'price')
    readonly_fields = ('display_image',)
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description', 'category', 'price')
        }),
        ('Характеристики', {
            'fields': ('weight', 'calories', 'is_vegetarian', 'is_spicy')
        }),
        ('Изображение', {
            'fields': ('image', 'display_image')
        }),
        ('Статус', {
            'fields': ('is_available',)
        })
    )

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" />', obj.image.url)
        return "Нет изображения"
    display_image.short_description = 'Изображение'
