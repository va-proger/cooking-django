from django.db import models
from .base import SlugMixin


class Tag(SlugMixin):
    title = models.CharField(max_length=255, verbose_name="Название тега")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
