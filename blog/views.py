# from django.conf import settings  # Импортируем настройки
# from django.core.mail import send_mail
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from pytils.translit import slugify

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


class BlogPostCreateView(CreateView):
    model = BlogPost
    template_name = "blog/blogpost_form.html"
    fields = ["title", "content", "preview", "is_published"]
    success_url = reverse_lazy("blog:post_list")

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save(commit=False)
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()
        return super().form_valid(form)


class BlogPostUpdateView(UpdateView):
    model = BlogPost
    template_name = "blog/blogpost_form.html"
    fields = ["title", "content", "preview", "is_published"]

    def get_success_url(self):
        return reverse("blog:post_detail", args=[self.object.pk])


class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = "blog/blogpost_confirm_delete.html"
    success_url = reverse_lazy("blog:post_list")
