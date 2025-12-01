from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, DetailView

from catalog.models import Product

class HomeTemplateView(TemplateView):
    template_name = 'catalog/home.html'

# def home(request):
#     return render(request, 'home.html')

class ContactsTemplateView(TemplateView):
    template_name = 'catalog/contacts.html'

# def contacts(request):
#     return render(request, 'contacts.html')

class ProductListView(ListView):
    model = Product

# def products_list(request):
#     products = Product.objects.all()
#     context = {'products': products}
#     return render(request, 'products_list.html', context)

class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'

# def products_detail(request, pk):
#     product = get_object_or_404(Product, id=pk)
#     context = {'product': product}
#     return render(request, 'product_detail.html', context)