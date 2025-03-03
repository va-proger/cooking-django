from django.db import models
from django.utils.text import slugify
from pytils.translit import slugify as translit_slugify
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


class PublishableModel(models.Model):
    is_published = models.BooleanField(default=True)

    class Meta:
        abstract = True