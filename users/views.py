import logging
import random
import string

import six
from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic.edit import CreateView, FormView, UpdateView

from .forms import CustomUserCreationForm, UserProfileForm
from .models import CustomUser


class CustomLoginView(LoginView):
    template_name = "users/login.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Вы успешно вошли в систему.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Неверное имя пользователя или пароль.")
        return super().form_invalid(form)


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "users/register.html"
    logger = logging.getLogger(__name__)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        logger.info(f"New user registered: {user.email}")

        # Генерация токена для верификации email
        token = account_activation_token.make_token(
            user
        )  # token = default_token_generator.make_token(user)
        logger.debug(f"Generated token: {token}")
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        verification_url = reverse_lazy(
            "verify_email", kwargs={"uidb64": uid, "token": token}
        )

        logger.debug(f"Verification URL generated: {verification_url}")

        # Отправка email для верификации
        try:
            send_mail(
                "Подтверждение регистрации",
                f"Пожалуйста, перейдите по ссылке для подтверждения регистрации: {self.request.build_absolute_uri(verification_url)}",
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            logger.info(f"Verification email sent to {user.email}")
        except Exception as e:
            logger.error(
                f"Failed to send verification email to {user.email}. Error: {str(e)}"
            )

        messages.success(
            self.request,
            "Регистрация успешна. Пожалуйста, проверьте вашу почту для подтверждения аккаунта.",
        )
        return super().form_valid(form)


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk)
            + six.text_type(timestamp)
            + six.text_type(user.is_active)
        )


account_activation_token = AccountActivationTokenGenerator()


class PasswordResetForm(forms.Form):
    email = forms.EmailField()


class PasswordResetView(FormView):
    template_name = "users/password_reset.html"
    form_class = PasswordResetForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        try:
            user = CustomUser.objects.get(email=email)
            new_password = "".join(
                random.choices(string.ascii_letters + string.digits, k=12)
            )
            user.password = make_password(new_password)
            user.save()

            send_mail(
                "Восстановление пароля",
                f"Ваш новый пароль: {new_password}",
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
        except CustomUser.DoesNotExist:
            pass  # Не сообщаем пользователю, что email не найден
        return super().form_valid(form)


logger = logging.getLogger(__name__)


def verify_email(request, uidb64, token):
    global uid
    logger.info(f"Attempting to verify email with uidb64: {uidb64} and token: {token}")
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        logger.info(f"Decoded uid: {uid}")
        user = CustomUser.objects.get(pk=uid)
        logger.info(f"User found: {user.email}")

        expected_token = account_activation_token.make_token(user)
        logger.debug(f"Expected token: {expected_token}, Received token: {token}")

        if not user.is_active and account_activation_token.check_token(user, token):
            logger.info(f"Token is valid for user: {user.email}")
            user.is_active = True
            user.save()
            login(request, user)
            logger.info(f"User {user.email} successfully verified and logged in")
            messages.success(
                request, "Ваш email успешно подтвержден. Вы вошли в систему."
            )
            return redirect("home")
        else:
            if user.is_active:
                logger.warning(f"User {user.email} is already active")
                messages.warning(request, "Ваш аккаунт уже активирован.")
            else:
                logger.warning(f"Invalid token for user: {user.email}")
                messages.error(request, "Ссылка для подтверждения недействительна.")
            return render(request, "users/activation_invalid.html")
    except (TypeError, ValueError, OverflowError) as e:
        logger.error(f"Error decoding uidb64: {str(e)}")
        user = None
    except CustomUser.DoesNotExist:
        logger.error(f"User not found for uid: {uid}")
        user = None

    logger.warning(f"Invalid verification link for uidb64: {uidb64}")
    messages.error(request, "Ссылка для подтверждения недействительна.")
    return render(request, "users/activation_invalid.html")


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = UserProfileForm
    template_name = "users/profile_edit.html"
    success_url = reverse_lazy("profile")

    def get_object(self, queryset=None):
        return self.request.user
