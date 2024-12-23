from django.urls import path

from .views import (
    BlogPostCreateView,
    BlogPostDeleteView,
    BlogPostDetailView,
    BlogPostListView,
    BlogPostUpdateView,
)

app_name = "blog"

urlpatterns = [
    # Маршрут для списка постов
    path("", BlogPostListView.as_view(), name="post_list"),
    # Маршрут для создания нового поста (важно, чтобы он был выше динамического маршрута)
    path("post/new/", BlogPostCreateView.as_view(), name="post_create"),
    # Маршрут для просмотра деталей поста
    path("post/<slug:slug>/", BlogPostDetailView.as_view(), name="post_detail"),
    # Маршрут для редактирования поста
    path("post/<slug:slug>/edit/", BlogPostUpdateView.as_view(), name="post_update"),
    # Маршрут для удаления поста
    path("post/<slug:slug>/delete/", BlogPostDeleteView.as_view(), name="post_delete"),
]
