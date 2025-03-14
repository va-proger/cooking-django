from django.db import models
from solo.models import SingletonModel
# Список популярных локалей
LOCALE_CHOICES = [
    ('ru-RU', 'Русский (Россия)'),
    ('en-US', 'English (US)'),
    ('de-DE', 'Deutsch (Deutschland)'),
    ('fr-FR', 'Français (France)'),
    ('es-ES', 'Español (España)'),
    ('zh-CN', '中文 (简体, 中国)'),
    ('ja-JP', '日本語 (日本)'),
    ('ar-SA', 'العربية (السعودية)'),
]

# Популярные форматы даты и времени
TIME_FORMAT_CHOICES = [
    ('d.m.Y', '31.12.2025'),
    ('Y-m-d', '2025-12-31'),
    ('m/d/Y', '12/31/2025'),
    ('d M Y', '31 Dec 2025'),
    ('D, d M Y', 'Fri, 31 Dec 2025'),
    ('l, d F Y', 'Friday, 31 December 2025'),
]

class SiteSettings(SingletonModel):

    maintenance_mode = models.BooleanField(
        default=False,
        verbose_name='Технический режим'
    )
    site_name = models.CharField(
        max_length=255,
        default='Мой Сайт',
        verbose_name='Название сайта'
    )
    # Логотип
    logo = models.ImageField(
        upload_to='logo/',
        blank=True,
        null=True,
        verbose_name="Логотип (JPG, PNG, WebP, SVG, AVIF)"
    )
    # Фавиконки
    favicon_ico = models.ImageField(upload_to='favicon/', blank=True, null=True, verbose_name="Favicon (ICO)")
    favicon_png_16 = models.ImageField(upload_to='favicon/', blank=True, null=True, verbose_name="Favicon (PNG 16x16)")
    favicon_png_32 = models.ImageField(upload_to='favicon/', blank=True, null=True, verbose_name="Favicon (PNG 32x32)")
    favicon_png_192 = models.ImageField(upload_to='favicon/', blank=True, null=True, verbose_name="Favicon (PNG 192x192)")
    favicon_png_512 = models.ImageField(upload_to='favicon/', blank=True, null=True, verbose_name="Favicon (PNG 512x512)")

    # Apple Touch Icon (для iOS)
    apple_touch_icon = models.ImageField(upload_to='favicon/', blank=True, null=True, verbose_name="Apple Touch Icon")

    # Safari mask icon (монохромная SVG)
    mask_icon = models.ImageField(upload_to='favicon/', blank=True, null=True, verbose_name="Safari Mask Icon")
    mask_icon_color = models.CharField(max_length=7, default="#000000", verbose_name="Цвет mask-icon")

    # Цвет статус-бара на мобильных
    theme_color = models.CharField(max_length=7, default="#ffffff", verbose_name="Цвет theme-color")

    # PWA manifest.json
    manifest_json = models.FileField(upload_to='favicon/', blank=True, null=True, verbose_name="Manifest.json")

    domains = models.TextField(
        default='example.com',
        help_text='Разделяйте домены запятыми',
        verbose_name='Домены'
    )
    main_phone = models.CharField(
        max_length=20,
        verbose_name='Основной телефон'
    )
    vk_url = models.URLField(
        blank=True,
        verbose_name='ВКонтакте'
    )
    github_url = models.URLField(
        blank=True,
        verbose_name='GitHub'
    )
    facebook_url = models.URLField(
        blank=True,
        verbose_name='Facebook'
    )
    instagram_url = models.URLField(
        blank=True,
        verbose_name='Instagram'
    )
    email = models.EmailField(
        verbose_name='Основной Email'
    )
    allow_indexing = models.BooleanField(
        default=True,
        verbose_name='Разрешить индексацию'
    )
    # Дата и время
    time_format = models.CharField(
        max_length=50,
        choices=TIME_FORMAT_CHOICES,
        default='d.m.Y',
        verbose_name='Формат даты и времени'
    )
    locale = models.CharField(
        max_length=10,
        choices=LOCALE_CHOICES,
        default='ru-RU',
        verbose_name='Локаль'
    )

    # Метрики
    google_analytics = models.TextField(
        blank=True,
        verbose_name="Google Analytics (код вставки в head)"
    )
    yandex_metrika = models.TextField(
        blank=True,
        verbose_name="Yandex Metrika (код вставки в head)"
    )

    def __str__(self):
        return "Настройки сайта"

    class Meta:
        verbose_name = 'Настройки сайта'