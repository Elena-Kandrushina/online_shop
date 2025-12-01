from django.contrib import admin
from .models import Blogs

# Register your models here.
@admin.register(Blogs)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'views_count')
    list_filter = ('created_at',)
    search_fields = ('title',)