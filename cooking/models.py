from django.db import models
from django.utils.text import slugify
from pytils.translit import slugify as translit_slugify
from tinymce.models import HTMLField

class Category(models.Model):
    ''' Категория новостей '''
    title = models.CharField(max_length=255, verbose_name="Название категории")
    slug = models.CharField(max_length=250, unique=True, blank=True)
    content = HTMLField(default='Скоро тут будет описание', verbose_name="Текст категории")
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    is_published = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)

    def generate_unique_slug(self):
        """ Создает уникальный slug из title, используя транслитерацию для русского текста """
        slug = translit_slugify(self.title) if any("а" <= ch <= "я" for ch in self.title.lower()) else slugify(
            self.title)
        unique_slug = slug
        num = 1
        while Category.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}-{num}"
            num += 1
        return unique_slug

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Tag(models.Model):
    ''' Теги Новостей '''
    title = models.CharField(max_length=255, verbose_name="Название тега")
    slug = models.CharField(max_length=250, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)

    def generate_unique_slug(self):
        """ Создает уникальный slug из title, используя транслитерацию для русского текста """
        slug = translit_slugify(self.title) if any("а" <= ch <= "я" for ch in self.title.lower()) else slugify(
            self.title)
        unique_slug = slug
        num = 1
        while Tag.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}-{num}"
            num += 1
        return unique_slug

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

class Post(models.Model):
    ''' Для новостных постов '''
    title = models.CharField(max_length=255, verbose_name="Заголовок статьи")
    slug = models.CharField(max_length=250, unique=True, blank=True)
    content = HTMLField(default='Скоро тут будет статья', verbose_name="Текст статьи")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    photo = models.ImageField(upload_to='photos/', blank=True, null=True, verbose_name="Изображение")
    watched = models.IntegerField(default=0, verbose_name="Просмотры")
    is_published = models.BooleanField(default=True, verbose_name="Публикация")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    tags = models.ManyToManyField(Tag, related_name='posts', verbose_name="Теги")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super().save(*args, **kwargs)

    def generate_unique_slug(self):
        """ Создает уникальный slug из title, используя транслитерацию для русского текста """
        slug = translit_slugify(self.title) if any("а" <= ch <= "я" for ch in self.title.lower()) else slugify(
            self.title)
        unique_slug = slug
        num = 1
        while Post.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{slug}-{num}"
            num += 1
        return unique_slug  # 👈 Добавляем return

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'



