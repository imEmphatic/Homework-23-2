from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Наименование категории")
    description = models.TextField(
        null=True, blank=True, verbose_name="Описание категории"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        max_length=50, verbose_name="Наименование", help_text="Введите наименование"
    )
    description = models.CharField(
        max_length=255,
        verbose_name="Краткое описание",
        help_text="Краткое описание",
        blank=True,
        null=True,
    )
    image_preview = models.ImageField(
        upload_to="product/photo",
        blank=True,
        null=True,
        verbose_name="Превью товара",
        help_text="Загрузите изображение товара",
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        help_text="Категория товара",
        blank=True,
        null=True,
        related_name="products",
    )
    purchase_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Стоимость", help_text="Цена за покупку"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания", help_text="Дата занесения в БД"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления",
        help_text="Дата последнего обновления",
    )

    manufactured_at = models.DateField(
        blank=True,
        verbose_name="Дата производства",
        help_text="Дата производства продукта",
        null=True,
    )
    views_count = models.IntegerField(default=0, verbose_name="Количество просмотров")

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["name", "category"]

    def __str__(self):
        return self.name


class Version(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="versions",
        verbose_name="Продукт",
    )
    version_number = models.CharField(max_length=50, verbose_name="Номер версии")
    version_name = models.CharField(max_length=100, verbose_name="Название версии")
    is_current = models.BooleanField(default=False, verbose_name="Текущая версия")

    class Meta:
        verbose_name = "Версия"
        verbose_name_plural = "Версии"
        ordering = ["-version_number"]

    def __str__(self):
        return f"{self.product.name} - {self.version_name} ({self.version_number})"

    def save(self, *args, **kwargs):
        if self.is_current:
            # Если эта версия отмечена как текущая, сбросим флаг у других версий этого продукта
            Version.objects.filter(product=self.product).exclude(pk=self.pk).update(is_current=False)
        super().save(*args, **kwargs)
