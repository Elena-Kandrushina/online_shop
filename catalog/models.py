from django.conf import settings
from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=150,
        help_text="Введите наименование категории",
        verbose_name="Наименование",
    )
    description = models.TextField(
        help_text="Добавьте описание категории",
        verbose_name="Описание",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"


class Product(models.Model):
    name = models.CharField(
        max_length=150,
        help_text="Введите наименование продукта",
        verbose_name="Наименование",
    )
    description = models.TextField(
        help_text="Добавьте описание продукта",
        verbose_name="Описание",
        blank=True,
        null=True,
    )
    image = models.ImageField(
        upload_to="images",
        help_text="Добавьте изображение продукта",
        verbose_name="Изображение",
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="products",
        blank=True,
        null=True,
    )
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата последнего изменения"
    )
    is_available = models.BooleanField(default=True)
    is_published = models.BooleanField(default=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Владелец',
        null=True,
        blank=True,
)

    def __str__(self):
        return f"{self.name} {self.category}"


    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"
        ordering = ["category", "name"]
        permissions = [
            ("can_unpublish_product", "Can unpublish product"),
            ("can_delete_product", "Can delete product"),
        ]
