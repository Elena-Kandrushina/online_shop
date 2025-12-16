from .models import Product

class ProductService:
    @classmethod
    def get_products_by_category(cls, category_id):
        return Product.objects.filter(
            category_id=category_id,
            is_available=True,
            is_published=True
        )
