from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, TemplateView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from catalog.forms import ProductForm
from catalog.models import Product


class HomeTemplateView(TemplateView):
    template_name = 'catalog/home.html'


class ContactsTemplateView(TemplateView):
    template_name = 'catalog/contacts.html'


class ProductListView(ListView):
    model = Product


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


