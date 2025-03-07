from django.db import models
from .base import SlugMixin, TimeStampedModel, PublishableModel, ImagesBaseModel, ContentBaseModel
from .category import Category
from .tag import Tag
from django.utils.safestring import mark_safe

class PostQuerySet(models.QuerySet):
    def popular(self):
        return self.filter(watched__gt=1000)

    def for_category(self, category):
        return self.filter(category=category)


class Post(SlugMixin, TimeStampedModel, PublishableModel, ImagesBaseModel, ContentBaseModel):
    objects = PostQuerySet.as_manager()
    title = models.CharField(max_length=255, verbose_name="Заголовок статьи")

    watched = models.IntegerField(default=0, verbose_name="Просмотры")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="posts", verbose_name="Категория"
    )
    tags = models.ManyToManyField(Tag, related_name="posts", blank=True, verbose_name="Теги")

    def __str__(self):
        return self.title

    def get_safe_preview(self):
        return mark_safe(self.preview_content)

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        indexes = [
            models.Index(fields=["-created_at", "is_published"]),
            models.Index(fields=["slug"], name="post_slug_idx"),
        ]
