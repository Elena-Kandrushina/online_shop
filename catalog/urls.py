from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import HomeTemplateView, ContactsTemplateView, ProductListView, ProductDetailView

app_name = CatalogConfig.name

urlpatterns = [
    path('', HomeTemplateView.as_view(), name='home'),
    path('contacts/', ContactsTemplateView.as_view(), name='contacts'),
    path('products_list/', ProductListView.as_view(), name='products_list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='products_detail'),

]