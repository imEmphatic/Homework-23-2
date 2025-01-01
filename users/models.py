from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    username = None  # Удаляем поле username
    email = models.EmailField(
        unique=True,
        verbose_name="Email",
        help_text="Введите ваш адрес электронной почты",
    )
    avatar = models.ImageField(
        upload_to="avatars/", blank=True, null=True, verbose_name="Аватар"
    )
    phone_number = models.CharField(
        max_length=15, blank=True, null=True, verbose_name="Номер телефона"
    )
    country = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Страна"
    )

    USERNAME_FIELD = "email"  # Используем email как поле для авторизации
    REQUIRED_FIELDS = ["username"]  # Оставляем пустым, если нет обязательных полей

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
