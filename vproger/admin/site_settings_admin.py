from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from solo.admin import SingletonModelAdmin
from unfold.admin import ModelAdmin
from vproger.models import SiteSettings

@admin.register(SiteSettings, site=admin.site)
class SiteSettingsAdmin(SingletonModelAdmin, ModelAdmin):
    fieldsets = (
        ("Основные настройки", {
            "fields": ("site_name", "logo", "domains", "main_phone", "email"),
            "classes": ("unfold-stack-item", "tab"),
            "description": "Основная информация о сайте и контакты"
        }),
        ("Фавиконки", {
            "fields": (
                "favicon_ico", "favicon_png_16", "favicon_png_32",
                "favicon_png_192", "favicon_png_512",
            ),
            "classes": ("unfold-stack-item", "tab"),
            "description": "Добавляется в футор и хеадер"
        }),
        ("Apple & Safari", {
            "fields": ("apple_touch_icon", "mask_icon", "mask_icon_color"),
            "classes": ("unfold-stack-item", "tab"),
            "description": "Параметры работы сайта"
        }),
        ("PWA", {
            "fields": ("manifest_json",),
            "classes": ("unfold-stack-item", "tab"),
            "description": "Манифест"
        }),
        ("Дополнительно", {
            "fields": ("theme_color",),
            "classes": ("unfold-stack-item", "tab"),
            "description": "Цвет темы"
        }),
        ("Социальные сети", {
            "fields": ("vk_url", "github_url", "facebook_url", "instagram_url"),
            "classes": ("unfold-stack-item", "collapse", "tab"),
            "description": "Ссылки на социальные сети"
        }),
        ("Технические настройки", {
            "fields": ("maintenance_mode", "allow_indexing", "time_format", "locale"),
            "classes": ("unfold-stack-item", "tab"),
            "description": "Параметры работы сайта"
        }),
        ("Метрики", {
            "fields": ("google_analytics", "yandex_metrika"),
            "classes": ("unfold-stack-item", "tab"),
            "description": "Добавляет метрики"
        }),

    )

    def logo_preview(self, obj):
        if obj.logo:
            return mark_safe(f'<img src="{obj.logo.url}" width="100">')
        return "Нет логотипа"

    logo_preview.short_description = "Логотип"


    readonly_fields = [ "logo_preview"]