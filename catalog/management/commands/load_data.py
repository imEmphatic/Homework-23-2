import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from catalog.models import Product, Category


class Command(BaseCommand):
    help = "Load data into the database from JSON files after clearing old data."

    @staticmethod
    def json_read_data():
        # Путь к файлу products.json в корне проекта
        file_path = os.path.join(settings.BASE_DIR, "products.json")
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def handle(self, *args, **options):
        # Удалите все продукты и категории
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Создайте списки для хранения объектов
        category_for_create = []
        product_for_create = []

        # Чтение данных из JSON
        data = Command.json_read_data()

        # Обходим все значения из данных
        for entry in data:
            model_name = entry["model"]
            fields = entry["fields"]

            if model_name == "catalog.category":
                category_for_create.append(
                    Category(
                        id=entry["pk"],
                        name=fields["name"],
                        description=fields.get("description", ""),
                    )
                )

        # Создаем объекты в базе с помощью метода bulk_create()
        Category.objects.bulk_create(category_for_create)

        # Обходим все значения продуктов из данных для получения информации об одном объекте
        for entry in data:
            model_name = entry["model"]
            fields = entry["fields"]

            if model_name == "catalog.product":
                category = Category.objects.get(pk=fields["category"])
                product_for_create.append(
                    Product(
                        id=entry["pk"],
                        name=fields["name"],
                        description=fields.get("description", ""),
                        image_preview=fields.get("image_preview", ""),
                        purchase_price=fields["purchase_price"],
                        created_at=fields["created_at"],
                        updated_at=fields["updated_at"],
                        category=category,
                    )
                )

        # Создаем объекты в базе с помощью метода bulk_create()
        Product.objects.bulk_create(product_for_create)

        self.stdout.write(
            self.style.SUCCESS("Successfully loaded data into the database.")
        )
