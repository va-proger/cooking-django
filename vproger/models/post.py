from django.conf import settings
from django.db import models
from django.db.models.fields import TextField
from django.urls import reverse

from .base import SlugMixin, TimeStampedModel, PublishableModel, ImagesBaseModel, ContentBaseModel
from .category import Category
from .tag import Tag
from django.utils.safestring import mark_safe
from markdownx.models import MarkdownxField

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
    detail_content_markdown = TextField(default="Скоро тут будет статья", blank=True, verbose_name="Текст статьи - markdown")
    tags = models.ManyToManyField(Tag, related_name="posts", blank=True, verbose_name="Теги")
    ''' поля для вк бота '''
    post_id = models.CharField(max_length=255, blank=True, editable=False, )
    vk_group_id = models.CharField(max_length=50,verbose_name="vk_group_id группы", default=settings.VK_GROUP_ID,  editable=False,)
    from_django = models.BooleanField(default=False, verbose_name="Из сайта")

    def get_absolute_url(self):
        return reverse('detail_post', args=[self.category.slug, self.slug])

    def save(self, *args, **kwargs):
        # Всегда устанавливаем значение из настроек
        self.vk_group_id = settings.VK_GROUP_ID
        super().save(*args, **kwargs)

    def __str__(self):
        fields = [str(self.vk_group_id), str(self.title)]
        return " - ".join(fields)

    def get_safe_preview(self):
        return mark_safe(self.preview_content)

    def tags_display(self):
        return ", ".join([tag.title for tag in self.tags.all()])

    tags_display.short_description = "Tags"

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        indexes = [
            models.Index(fields=["-created_at", "is_published"]),
            models.Index(fields=["slug"], name="post_slug_idx"),
        ]
