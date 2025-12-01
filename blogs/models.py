from django.db import models


class Blogs(models.Model):
    title = models.CharField(
        max_length=250,
        help_text="Введите заголовок",
        verbose_name="Заголовок",
    )

    content = models.TextField(
        help_text="Добавьте содержимое",
        verbose_name="Содержимое",
        blank=True,
        null=True,
    )
    image = models.ImageField(
        upload_to="images",
        help_text="Добавьте изображение (превью)",
        verbose_name="Изображение",
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')
    views_count = models.PositiveIntegerField(default=0, verbose_name='Количество просмотров')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Блоговая запись'
        verbose_name_plural = 'Блоговые записи'
        ordering = ['-created_at']





