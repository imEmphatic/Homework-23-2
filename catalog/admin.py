from django.contrib import admin

from catalog.models import Category, Product, Version


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "purchase_price",
        "category",
        "publication_status",
        "description",
    )
    list_filter = ("category", "publication_status")
    search_fields = ("name", "description")
    readonly_fields = ("views_counter", "created_at", "updated_at")
    permissions = ["catalog.change_product"]

    def get_readonly_fields(self, request, obj=None):
        if obj and not request.user.has_perm("catalog.can_change_product_description"):
            return self.readonly_fields + ("description",)
        return self.readonly_fields

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        if not obj.owner:
            obj.owner = request.user
        super().save_model(request, obj, form, change)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ("product", "version_number", "version_name", "is_current")
    list_filter = ("product", "is_current")
