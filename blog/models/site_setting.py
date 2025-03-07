from django.db import models
from solo.models import SingletonModel
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
    time_format = models.CharField(
        max_length=50,
        default='H:i',
        verbose_name='Формат времени'
    )
    locale = models.CharField(
        max_length=10,
        default='ru-RU',
        verbose_name='Локаль'
    )

    def __str__(self):
        return "Настройки сайта"

    class Meta:
        verbose_name = 'Настройки сайта'