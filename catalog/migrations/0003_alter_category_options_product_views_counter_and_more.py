# Generated by Django 5.1.1 on 2024-09-20 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0002_product_manufactured_at_alter_product_created_at_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="category",
            options={
                "ordering": ["name"],
                "verbose_name": "Категория",
                "verbose_name_plural": "Категории",
            },
        ),
        migrations.AddField(
            model_name="product",
            name="views_counter",
            field=models.PositiveIntegerField(
                default=0,
                help_text="Количество просмотров",
                verbose_name="Счетчик просмотров",
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="description",
            field=models.TextField(
                blank=True, null=True, verbose_name="Описание категории"
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="name",
            field=models.CharField(
                max_length=100, verbose_name="Наименование категории"
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True,
                help_text="Дата занесения в БД",
                verbose_name="Дата создания",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True,
                help_text="Дата последнего обновления",
                verbose_name="Дата обновления",
            ),
        ),
    ]