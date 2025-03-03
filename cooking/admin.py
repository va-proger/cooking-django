from django.contrib import admin
from django.db import models
from unfold.contrib.forms.widgets import WysiwygWidget
from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from .models import Category, Post, Tag
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group



class PostAdmin(ModelAdmin):
    list_display = ('id', 'title', 'slug',  'watched', 'category',  'is_published', 'created_at', 'updated_at')
    list_display_links = ['id', 'title',]
    list_editable = ('is_published',)
    readonly_fields = ('watched',)
    list_filter = ('is_published', 'tags', 'category', 'created_at', 'updated_at', )

    formfield_overrides = {
        models.TextField: {
            'widget': WysiwygWidget,
        },
    }

class CategoryAdmin(ModelAdmin):
    list_display = ('id', 'title', 'slug', 'is_published')
    list_display_links = ('id', 'title',)

    list_editable = ('is_published',)
    formfield_overrides = {
        models.TextField: {
            'widget': WysiwygWidget,
        },
    }
class TagAdmin(ModelAdmin):
    formfield_overrides = {
            models.TextField: {
                "widget": WysiwygWidget,
            }
        }

admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)

''' пользователи и группы '''
admin.site.unregister(User)
admin.site.unregister(Group)
@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    ''' Кастомизируем стандартного пользователя '''
    # Поля в списке пользователей
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_editable = ('is_staff', 'is_active',)
    # Поиск по полям
    search_fields = ('username', 'email', 'first_name', 'last_name')
    # Forms loaded from `unfold.forms`
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass