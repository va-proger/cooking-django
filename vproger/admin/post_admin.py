from django.contrib import admin
from django.db import models
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget
from import_export.admin import ImportExportModelAdmin
from vproger.models import Post
from vk_bot.tasks import import_vk_posts
from vk_bot.services import VKService
from markdownx.widgets import AdminMarkdownxWidget
from markdownx.admin import MarkdownxModelAdmin


class PostAdmin(ModelAdmin):
    list_display = ("id", "title", "slug", "watched", "category", 'tags_display', "is_published", "created_at", "updated_at")
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
        ('Основное', {"classes": ["tab"], "fields": ['detail_image', 'detail_content', 'detail_content_markdown']}),
        ('Дополнительно', {"classes": ["tab"], "fields": ['watched', 'category', 'tags']}),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Применяем AdminMarkdownxWidget только к полю detail_content_markdown
        if 'detail_content_markdown' in form.base_fields:
            form.base_fields['detail_content_markdown'].widget = AdminMarkdownxWidget()
        return form

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

admin.site.register(Post, PostAdmin, )
