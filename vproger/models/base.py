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

from django.db import models
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe

class SeoMixin(models.Model):
    seo_title = models.CharField(
        max_length=255, blank=True, verbose_name="SEO Title",
        help_text="Заголовок для поисковых систем. Если не заполнено, будет использоваться title."
    )
    seo_description = models.TextField(
        blank=True, verbose_name="SEO Description",
        help_text="Описание для поисковых систем. Если не заполнено, будет автоматически сформировано из контента."
    )
    seo_keywords = models.CharField(
        max_length=255, blank=True, verbose_name="SEO Keywords",
        help_text="Ключевые слова через запятую."
    )
    seo_canonical = models.URLField(
        blank=True, null=True, verbose_name="Canonical URL",
        help_text="Канонический URL (если не установлен, будет использоваться get_absolute_url)."
    )

    class Meta:
        abstract = True

    def get_seo_title(self):
        return self.seo_title if self.seo_title else self.title

    def get_seo_description(self):
        if self.seo_description:
            return self.seo_description
        content = strip_tags(self.detail_content_markdown)[:150] + "..."
        return content if content else "Описание отсутствует."

    def get_canonical_url(self):
        return self.seo_canonical if self.seo_canonical else self.get_absolute_url()

    def get_meta_tags(self):
        """Генерирует мета-теги для шаблона"""
        return mark_safe(f"""
            <title>{self.get_seo_title()}</title>
            <meta name="description" content="{self.get_seo_description()}">
            <meta name="keywords" content="{self.seo_keywords}">
            <link rel="canonical" href="{self.get_canonical_url()}">
        """)
