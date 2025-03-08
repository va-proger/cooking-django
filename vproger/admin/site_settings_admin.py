from django.contrib import admin
from solo.admin import SingletonModelAdmin
from unfold.admin import ModelAdmin
from vproger.models import SiteSettings

@admin.register(SiteSettings, site=admin.site)
class SiteSettingsAdmin(SingletonModelAdmin, ModelAdmin):
    fieldsets = (
        ("Основные настройки", {
            "fields": ("site_name", "domains", "main_phone", "email"),
            "classes": ("unfold-stack-item",),
            "description": "Основная информация о сайте и контакты"
        }),
        ("Социальные сети", {
            "fields": ("vk_url", "github_url", "facebook_url", "instagram_url"),
            "classes": ("unfold-stack-item", "collapse"),
            "description": "Ссылки на социальные сети"
        }),
        ("Технические настройки", {
            "fields": ("maintenance_mode", "allow_indexing", "time_format", "locale"),
            "classes": ("unfold-stack-item",),
            "description": "Параметры работы сайта"
        }),
    )
