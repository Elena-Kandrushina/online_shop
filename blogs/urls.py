from django.urls import path
from blogs.apps import BlogsConfig
from blogs.views import HomeTemplateView, BlogsListView, BlogsDetailView, BlogsCreateView, BlogsUpdateView, \
    BlogsDeleteView

app_name = BlogsConfig.name

urlpatterns = [
    path('', HomeTemplateView.as_view(), name='home'),
    path('blogs_list/', BlogsListView.as_view(), name='blogs_list'),
    path('blogs/<int:pk>/', BlogsDetailView.as_view(), name='blogs_detail'),
    path('blogs/create/', BlogsCreateView.as_view(), name='blogs_create'),
    path('blogs/<int:pk>/edit/', BlogsUpdateView.as_view(), name='blogs_edit'),
    path('blogs/<int:pk>/delete/', BlogsDeleteView.as_view(), name='blogs_delete'),
]

