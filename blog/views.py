from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from blog.forms import BlogForm
from blog.models import Blog
from mailing.services import cache_blog


class BlogListView(ListView):
    model = Blog

    def get_queryset(self):
        return cache_blog()


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogCreateView(CreateView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('blog:blog_list')


class BlogUpdateView(UpdateView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('blog:list')

    def get_success_url(self):
        return reverse('blog:blog_view', args=[self.kwargs.get('pk')])


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:blog_list')
