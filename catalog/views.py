from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from catalog.forms import ProductForm
from catalog.models import Product, Category
from catalog.services import ProductService


class HomeTemplateView(TemplateView):
    template_name = 'catalog/home.html'



class ContactsTemplateView(TemplateView):
    template_name = 'catalog/contacts.html'


class ProductListView(ListView):
    model = Product

    def get_queryset(self):
        queryset = cache.get('products_queryset')
        if not queryset:
            queryset = super().get_queryset()
            cache.set('products_queryset', queryset, 60 * 15)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        context['categories'] = categories
        category_id = self.request.GET.get('category_id')

        if category_id:
            category = get_object_or_404(Category, pk=category_id)
            context['selected_category_name'] = category.name
        else:
            context['selected_category_name'] = None
        context['selected_category_id'] = category_id
        return context


@method_decorator(cache_page(60 * 15), name='dispatch')
class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    context_object_name = 'product'



class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_create.html'
    success_url = reverse_lazy('catalog:products_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_edit.html'
    success_url = reverse_lazy('catalog:products_list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner != request.user:
            return HttpResponseForbidden("Вы не являетесь владельцем этого продукта.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if 'is_published' in form.changed_data:
            if not self.request.user.has_perm('catalog.can_unpublish_product'):
                return HttpResponseForbidden("У вас нет прав менять статус публикации.")
        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:products_list')
    permission_required = ('catalog.can_delete_product',)

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        user = request.user
        is_owner = (obj.owner is not None) and (obj.owner == user)
        is_moderator = user.has_perm('catalog.can_delete_product')

        if not (is_owner or is_moderator):
            return HttpResponseForbidden("Удалять этот продукт могут только владелец или модератор.")
        return super().dispatch(request, *args, **kwargs)


class CategoryProductsView(ListView):
    model = Product
    template_name = 'catalog/category_products.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        return ProductService.get_products_by_category(category_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
        context['category'] = category
        return context