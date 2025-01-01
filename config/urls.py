from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.views.generic import RedirectView

from users import views as user_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("catalog.urls", namespace="catalog")),
    path("blog/", include("blog.urls", namespace="blog")),
    path("register/", user_views.RegisterView.as_view(), name="register"),
    path(
        "login/", user_views.CustomLoginView.as_view(), name="login"
    ),  # Updated this line
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path(
        "password_reset/", user_views.PasswordResetView.as_view(), name="password_reset"
    ),
    path("verify/<uidb64>/<token>/", user_views.verify_email, name="verify_email"),
    path(
        "profile/edit/", user_views.UserProfileUpdateView.as_view(), name="profile_edit"
    ),
    path("", RedirectView.as_view(url="/products/", permanent=True), name="home"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
