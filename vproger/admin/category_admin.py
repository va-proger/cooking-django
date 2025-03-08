from django.contrib import admin
from django.db import models
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget
from vproger.models import Category


class CategoryAdmin(ModelAdmin):
    field_order = ["title", "preview_image", "detail_image"]
    list_display = ("id", "title", "slug", "is_published")
    list_display_links = ("id", "title")
    list_editable = ("is_published",)

    formfield_overrides = {
        models.TextField: {"widget": WysiwygWidget},
    }

    fieldsets = (
        ('Основная информация', {"classes": ["tab"], "fields": ['is_published', 'title', 'slug']}),
        ('Анонс', {"classes": ["tab"], "fields": ['preview_image', 'preview_content']}),
        ('Основное', {"classes": ["tab"], "fields": ['detail_image', 'detail_content']}),
    )


admin.site.register(Category, CategoryAdmin)
