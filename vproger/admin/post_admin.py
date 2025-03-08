from django.contrib import admin
from django.db import models
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget
from import_export.admin import ImportExportModelAdmin
from vproger.models import Post
from vk_bot.tasks import import_vk_posts
from vk_bot.services import VKService

class PostAdmin(ModelAdmin):
    list_display = ("id", "title", "slug", "watched", "category", "is_published", "created_at", "updated_at")
    list_display_links = ["id", "title"]
    list_editable = ("is_published",)
    readonly_fields = ("watched", "updated_at", "created_at")
    list_filter = ("is_published", "tags", "category", "created_at", "updated_at")
    readonly_fields = ('vk_group_id','watched')
    formfield_overrides = {
        models.TextField: {"widget": WysiwygWidget},
    }

    fieldsets = (
        ('Основная информация', {"classes": ["tab"], "fields": ['is_published', 'title', 'slug', ]}),
        ('Анонс', {"classes": ["tab"], "fields": ['preview_image', 'preview_content']}),
        ('Основное', {"classes": ["tab"], "fields": ['detail_image', 'detail_content']}),
        ('Дополнительно', {"classes": ["tab"], "fields": ['watched', 'category']}),
    )

admin.site.register(Post, PostAdmin)
