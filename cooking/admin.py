from django.contrib import admin
from .models import Category, Post, Tag


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug',  'watched', 'category',  'is_published', 'created_at', 'updated_at')
    list_display_links = ['id', 'title',]
    list_editable = ('is_published',)
    readonly_fields = ('watched',)
    list_filter = ('is_published', 'tags', 'category', 'created_at', 'updated_at', )


admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
