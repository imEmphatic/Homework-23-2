from django.db import models
from django.urls import reverse


class BlogPost(models.Model):
    objects = None
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    slug = models.CharField(max_length=200, unique=True, verbose_name="Slug")
    content = models.TextField(verbose_name="Содержимое")
    preview = models.ImageField(
        upload_to="blog_previews/", verbose_name="Превью", null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_published = models.BooleanField(default=False, verbose_name="Опубликовано")
    views_count = models.PositiveIntegerField(
        default=0, verbose_name="Количество просмотров"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Блоговая запись"
        verbose_name_plural = "Блоговые записи"
