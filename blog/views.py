from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.mail import send_mail
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django.views.decorators.cache import never_cache
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .models import BlogPost


class BlogPostListView(ListView):
    model = BlogPost
    template_name = "blog/blogpost_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True)


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = "blog/blogpost_detail.html"
    context_object_name = "post"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views_count += 1

        if obj.views_count == 100:
            send_mail(
                "Поздравляем с достижением!",
                f'Статья "{obj.title}" достигла 100 просмотров!',
                settings.DEFAULT_FROM_EMAIL,
                ["aleksey.bedrinsky@yandex.ru"],
                fail_silently=True,
            )

        obj.save()
        return obj


@method_decorator(never_cache, name="dispatch")
class BlogPostCreateView(UserPassesTestMixin, CreateView):
    model = BlogPost
    template_name = "blog/blogpost_form.html"
    fields = ["title", "content", "preview", "is_published"]

    def test_func(self):
        return self.request.user.groups.filter(name="Content Managers").exists()

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save(commit=False)
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)


class BlogPostUpdateView(UserPassesTestMixin, UpdateView):
    model = BlogPost
    template_name = "blog/blogpost_form.html"
    fields = ["title", "content", "preview", "is_published"]

    def test_func(self):
        return self.request.user.groups.filter(name="Content Managers").exists()

    def get_success_url(self):
        return reverse("blog:post_detail", args=[self.object.slug])


class BlogPostDeleteView(UserPassesTestMixin, DeleteView):
    model = BlogPost
    template_name = "blog/blogpost_confirm_delete.html"
    success_url = reverse_lazy("blog:post_list")

    def test_func(self):
        return self.request.user.groups.filter(name="Content Managers").exists()
