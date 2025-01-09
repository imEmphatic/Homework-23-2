from django import forms

from .models import Product, Version


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.BooleanField):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"


class VersionForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Version
        fields = ["product", "version_number", "version_name", "is_current"]

    def clean(self):
        cleaned_data = super().clean()
        is_current = cleaned_data.get("is_current")
        product = cleaned_data.get("product")

        if is_current and product:
            # Проверяем, есть ли уже активная версия для этого продукта
            existing_current = (
                Version.objects.filter(product=product, is_current=True)
                .exclude(pk=self.instance.pk)
                .exists()
            )
            if existing_current:
                raise forms.ValidationError(
                    "Для этого продукта уже есть активная версия. Пожалуйста, выберите только одну активную версию."
                )

        return cleaned_data


class ProductForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "image_preview",
            "category",
            "purchase_price",
            "views_counter",
            "manufactured_at",
        ]

    def clean_name(self):
        return self.clean_field("name")

    def clean_description(self):
        return self.clean_field("description")

    def clean_field(self, field_name):
        data = self.cleaned_data[field_name]
        forbidden_words = [
            "казино",
            "криптовалюта",
            "крипта",
            "биржа",
            "дешево",
            "бесплатно",
            "обман",
            "полиция",
            "радар",
        ]

        for word in forbidden_words:
            if word in data.lower():
                raise forms.ValidationError(
                    f"Запрещенное слово '{word}' не может быть использовано."
                )

        return data
