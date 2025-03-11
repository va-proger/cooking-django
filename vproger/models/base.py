from django.db import models
from django.db.models.fields import TextField
from .utils.slugs import generate_unique_slug

class SlugMixin(models.Model):
    slug = models.CharField(max_length=250, unique=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self, self.title)
        super().save(*args, **kwargs)


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class ImagesBaseModel(models.Model):
    preview_image = models.ImageField(
        upload_to="photos/preview/", blank=True, null=True, verbose_name="Изображения - анонс"
    )
    detail_image = models.ImageField(
        upload_to="photos/detail/", blank=True, null=True, verbose_name="Изображение - детальной"
    )

    class Meta:
        abstract = True

class ContentBaseModel(models.Model):
    preview_content = TextField(default="Скоро тут будет статья", blank=True, verbose_name="Текст статьи - анонс")
    detail_content = TextField(default="Скоро тут будет статья", verbose_name="Текст статьи - детальный")

    class Meta:
        abstract = True

class PublishableModel(models.Model):
    is_published = models.BooleanField(default=True, verbose_name="Активно")

    class Meta:
        abstract = True
