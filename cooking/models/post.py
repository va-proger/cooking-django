from django.db import models
from django.db.models.fields import TextField
# from tinymce.models import HTMLField
from .base import SlugMixin, TimeStampedModel, PublishableModel
from .category import Category
from .tag import Tag


class PostQuerySet(models.QuerySet):
    def popular(self):
        return self.filter(watched__gt=1000)

    def for_category(self, category):
        return self.filter(category=category)

class Post(SlugMixin, TimeStampedModel, PublishableModel):
    objects = PostQuerySet.as_manager()
    title = models.CharField(max_length=255, verbose_name="Заголовок статьи")
    content = TextField(default='Скоро тут будет статья', verbose_name="Текст статьи")
    photo = models.ImageField(upload_to='photos/', blank=True, null=True, verbose_name="Изображение")
    watched = models.IntegerField(default=0, verbose_name="Просмотры")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    tags = models.ManyToManyField(Tag, related_name='posts', verbose_name="Теги")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        indexes = [
            models.Index(fields=['-created_at', 'is_published']),
            models.Index(fields=['slug'], name='post_slug_idx')
        ]