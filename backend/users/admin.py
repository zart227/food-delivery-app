from django.contrib import admin
from .models import User, Role, UserRole


class UserRoleInline(admin.TabularInline):
    model = UserRole  # Промежуточная модель
    extra = 1  # Количество пустых строк для добавления новых записей


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "is_active", "is_staff", "is_verified")
    list_filter = ("is_active", "is_staff", "is_verified")
    search_fields = ("username", "email")
    inlines = [UserRoleInline]  # Добавляем inline-редактор для управления ролями
    exclude = ("roles",)  # Исключаем поле roles, чтобы избежать конфликтов


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name", "description")  # Настройка отображения ролей
    search_fields = ("name",)


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "role",
        "assigned_at",
    )  # Настройка отображения промежуточной модели
    list_filter = ("role",)
    search_fields = ("user__username", "role__name")
