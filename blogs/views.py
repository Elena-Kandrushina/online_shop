from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView, DeleteView

from blogs.models import Blogs

class HomeTemplateView(TemplateView):
    template_name = 'blogs/home.html'


class BlogsListView(ListView):
    model = Blogs
    template_name = 'blogs/blogs_list.html'
    context_object_name = 'blogs'

    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)


class BlogsDetailView(DetailView):
    model = Blogs
    template_name = 'blogs/blogs_detail.html'
    context_object_name = 'blog'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views_count = obj.views_count + 1
        obj.save(update_fields=['views_count'])
        return obj

class BlogsCreateView(CreateView):
    model = Blogs
    fields = ['title', 'content', 'image', 'is_published', 'views_count']
    template_name = 'blogs/blogs_create.html'
    success_url = reverse_lazy('blogs:blogs_list')


class BlogsUpdateView(UpdateView):
    model = Blogs
    fields = ['title', 'content', 'image', 'is_published', 'views_count']
    template_name = 'blogs/blogs_edit.html'
    success_url = reverse_lazy('blogs:blogs_list')

class BlogsDeleteView(DeleteView):
    model = Blogs
    template_name = 'blogs/blogs_confirm_delete.html'
    success_url = reverse_lazy('blogs:blogs_list')