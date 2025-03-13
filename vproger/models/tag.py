from django.db import models
from django.urls import reverse

from .base import SlugMixin


class Tag(SlugMixin):
    title = models.CharField(max_length=255, verbose_name="Название тега")

    def get_absolute_url(self):
        return reverse('tag_posts', args=[self.slug])

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
