from django.db import models
from django.db.models.fields import TextField
from django.urls import reverse

from .base import SlugMixin, PublishableModel, ImagesBaseModel, ContentBaseModel


class Category(SlugMixin, PublishableModel, ImagesBaseModel, ContentBaseModel):
    title = models.CharField(max_length=255, verbose_name="Название категории")

    def get_absolute_url(self):
        return reverse('category_posts', args=[self.slug])

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
