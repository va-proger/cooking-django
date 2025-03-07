from django.contrib import admin
from django.db import models
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget
from import_export.admin import ImportExportModelAdmin
from blog.models import Post

class PostAdmin(ModelAdmin):
    list_display = ("id", "title", "slug", "watched", "category", "is_published", "created_at", "updated_at")
    list_display_links = ["id", "title"]
    list_editable = ("is_published",)
    readonly_fields = ("watched",)
    list_filter = ("is_published", "tags", "category", "created_at", "updated_at")

    formfield_overrides = {
        models.TextField: {"widget": WysiwygWidget},
    }

    

admin.site.register(Post, PostAdmin)
