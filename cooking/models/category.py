from django.db import models
from django.db.models.fields import TextField
from .base import SlugMixin, PublishableModel

class Category(SlugMixin, PublishableModel):
    title = models.CharField(max_length=255, verbose_name="Название категории")
    content = TextField(default='Скоро тут будет описание', verbose_name="Текст категории")
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'