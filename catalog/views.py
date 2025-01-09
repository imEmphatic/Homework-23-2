import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import get_template
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page, never_cache
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import ProductForm, VersionForm
from .models import Product, Version
from .services import get_cached_categories


class ProductListView(ListView):
    model = Product
    template_name = "product_list.html"
    context_object_name = "object_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = get_cached_categories()
        for product in context["object_list"]:
            product.active_version = product.versions.filter(is_current=True).first()
        return context


class CategoryListView(LoginRequiredMixin, ListView):
    template_name = "category_list.html"
    context_object_name = "categories"

    def get_queryset(self):
        return get_cached_categories()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = json.dumps(
            list(self.get_queryset().values()), cls=DjangoJSONEncoder
        )
        return context


@method_decorator(cache_page(60 * 15), name="dispatch")  # кэшируем на 15 минут
class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"

    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg)
        obj = get_object_or_404(Product, pk=pk)
        obj.views_counter += 1
        obj.save()
        return obj


@method_decorator(never_cache, name="dispatch")
class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "product_form.html"
    success_url = reverse_lazy("catalog:catalog_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, "Продукт успешно создан!")
        return response


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "product_form.html"

    def test_func(self):
        product = self.get_object()
        return self.request.user == product.owner or self.request.user.has_perm(
            "catalog.change_product"
        )

    def get_success_url(self):
        return reverse("catalog:catalog_detail", args=[self.kwargs.get("pk")])

    def handle_no_permission(self):
        messages.error(
            self.request, "У вас нет прав для редактирования этого продукта."
        )
        return redirect("catalog:catalog_detail", pk=self.kwargs.get("pk"))


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "product_confirm_delete.html"
    success_url = reverse_lazy("catalog:catalog_list")


class VersionCreateView(LoginRequiredMixin, CreateView):
    model = Version
    form_class = VersionForm
    template_name = "version_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Версия успешно создана.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Пожалуйста, исправьте ошибки в форме.")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse("catalog:catalog_detail", kwargs={"pk": self.object.product.pk})


class VersionUpdateView(LoginRequiredMixin, UpdateView):
    model = Version
    form_class = VersionForm
    template_name = "version_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Версия успешно обновлена.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Пожалуйста, исправьте ошибки в форме.")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse("catalog:catalog_detail", kwargs={"pk": self.object.product.pk})


class VersionDeleteView(LoginRequiredMixin, DeleteView):
    model = Version
    template_name = "version_confirm_delete.html"

    def get_success_url(self):
        return reverse("catalog:catalog_detail", kwargs={"pk": self.object.product.pk})


def test_cache(request):
    return HttpResponse("Test cache view")
