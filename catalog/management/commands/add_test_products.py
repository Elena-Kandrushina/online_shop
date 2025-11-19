from django.core.management.base import BaseCommand
from catalog.models import Product, Category


class Command(BaseCommand):
    help = "Add test products to the database"

    def handle(self, *args, **kwargs):
        Product.objects.all().delete()
        Category.objects.all().delete()
        category, _ = Category.objects.get_or_create(
            name="Спортинвентарь", description="Инвентарь для спорта, отдыха и туризма"
        )

        products = [
            {
                "name": "Велосипед",
                "category": category,
                "prise": "32000.0",
                "created_at": "2025-11-19",
            },
            {
                "name": "Самокат",
                "category": category,
                "prise": "22000.0",
                "created_at": "2025-11-19",
            },
        ]

        for product in products:
            product, created = Product.objects.get_or_create(**product)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Successfully added product: {product.name}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Product already exists: {product.name}")
                )
