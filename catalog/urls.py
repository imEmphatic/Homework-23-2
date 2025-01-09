from django.urls import path

from . import views

app_name = "catalog"

urlpatterns = [
    path("products/", views.ProductListView.as_view(), name="catalog_list"),
    path(
        "products/<int:pk>/", views.ProductDetailView.as_view(), name="catalog_detail"
    ),
    path("products/create/", views.ProductCreateView.as_view(), name="catalog_create"),
    path(
        "products/<int:pk>/update/",
        views.ProductUpdateView.as_view(),
        name="catalog_update",
    ),
    path(
        "products/<int:pk>/delete/",
        views.ProductDeleteView.as_view(),
        name="catalog_delete",
    ),
    path("version/create/", views.VersionCreateView.as_view(), name="version_create"),
    path(
        "version/<int:pk>/update/",
        views.VersionUpdateView.as_view(),
        name="version_update",
    ),
    path(
        "version/<int:pk>/delete/",
        views.VersionDeleteView.as_view(),
        name="version_delete",
    ),
    path("test-cache/", views.test_cache, name="test_cache"),
    path("categories/", views.CategoryListView.as_view(), name="category_list"),
]
