from django.db import models
from pytils.translit import slugify


def generate_unique_slug(instance, source_text):
    """Генерация уникального slug для любой модели"""
    slug = _generate_base_slug(source_text)
    ModelClass = instance.__class__

    num = 1
    unique_slug = slug
    while ModelClass.objects.filter(slug=unique_slug).exclude(pk=instance.pk).exists():
        unique_slug = f"{slug}-{num}"
        num += 1
    return unique_slug


def _generate_base_slug(text):
    """Генерация базового slug с поддержкой кириллицы"""
    if any("а" <= ch <= "я" for ch in text.lower()):
        from pytils.translit import slugify as translit_slugify
        return translit_slugify(text)
    return slugify(text)