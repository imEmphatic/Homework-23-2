from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from catalog.views import (
    ContactsView,
    HomeView,
    ProductCreateView,
    ProductDeleteView,
    ProductDetailView,
    ProductListView,
    ProductUpdateView,
    VersionCreateView,
    VersionDeleteView,
    VersionUpdateView,
)

app_name = "catalog"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path("products/", ProductListView.as_view(), name="catalog_list"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="catalog_detail"),
    path("products/create/", ProductCreateView.as_view(), name="catalog_create"),
    path(
        "products/<int:pk>/update/", ProductUpdateView.as_view(), name="catalog_update"
    ),
    path(
        "products/<int:pk>/delete/", ProductDeleteView.as_view(), name="catalog_delete"
    ),
    path("version/create/", VersionCreateView.as_view(), name="version_create"),
    path(
        "version/<int:pk>/update/", VersionUpdateView.as_view(), name="version_update"
    ),
    path(
        "version/<int:pk>/delete/", VersionDeleteView.as_view(), name="version_delete"
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
