from django.db import models
from django.db.models import TextField

from . import Post
from .base import SlugMixin, PublishableModel


class Comment(SlugMixin, PublishableModel ):
    title = models.CharField(max_length=255, verbose_name="Заголовок статьи")
    comment = TextField( verbose_name="Комментарий")
    post = models.ForeignKey(
        Post, on_delete=models.PROTECT, related_name="post", verbose_name="Пост"
    )
    def __str__(self):
        fields = [str(self.title)]
        return " - ".join(fields)


    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

