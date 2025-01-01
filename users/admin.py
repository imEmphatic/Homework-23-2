from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("email", "phone_number", "country", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("avatar", "phone_number", "country")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


# Регистрация модели и кастомного админа
admin.site.register(CustomUser, CustomUserAdmin)
