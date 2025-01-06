from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ["email", "username", "is_staff", "is_active"]

    # Убираем дублирование полей
    fieldsets = UserAdmin.fieldsets + (
        (
            None,
            {"fields": ("avatar", "phone_number", "country")},
        ),  # Убедитесь, что эти поля не добавляются повторно
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            None,
            {"fields": ("avatar", "phone_number", "country")},
        ),  # Тоже проверяем, чтобы не было дублирования
    )

    filter_horizontal = ("user_permissions",)


admin.site.register(CustomUser, CustomUserAdmin)
