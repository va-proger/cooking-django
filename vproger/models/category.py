from django.db import models
from django.db.models.fields import TextField
from .base import SlugMixin, PublishableModel, ImagesBaseModel, ContentBaseModel


class Category(SlugMixin, PublishableModel, ImagesBaseModel, ContentBaseModel):
    title = models.CharField(max_length=255, verbose_name="Название категории")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
