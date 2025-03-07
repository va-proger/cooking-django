from django.contrib import admin, messages
from django.http import HttpRequest
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from unfold.admin import ModelAdmin
from unfold.decorators import action

from vk_bot.tasks import import_vk_posts
from vk_bot.models import VKPost
from vk_bot.services import VKService

csrf_protect_m = method_decorator(csrf_protect)


@admin.register(VKPost)
class VKPostAdmin(ModelAdmin):
    list_display = ('post_id', 'date', 'vk_group_id', 'from_django')
    actions_on_top = True    # Показывать действия над таблицей
    actions_on_bottom = True # Показывать действия под таблицей
    # Define actions directly in the ModelAdmin class
    action(description="📥 Импортировать посты из VK")
    @staticmethod
    def import_vk_posts_action(request, queryset):
        task = import_vk_posts.delay()
        messages.success(request, f"Импорт запущен! Задача ID: {task.id}")
        return redirect("admin:vk_bot_vkpost_changelist")

    action(description="🚀 Опубликовать выбранное в VK")
    @staticmethod
    def post_to_vk_action(request, queryset):
        vk = VKService()
        count = 0
        for post in queryset:
            vk.post_to_group(post.text)
            count += 1
        messages.success(request, f"{count} постов отправлено в VK!")

    action(description="❌ Удалить выбранное из VK")
    @staticmethod
    def delete_post_action(request, queryset):
        vk = VKService()
        count = 0
        for post in queryset:
            if post.post_id:
                vk.delete_post(post.post_id)
                count += 1
        messages.success(request, f"{count} постов удалено из VK!")



    # Register the actions
    actions = ["import_vk_posts_action", "post_to_vk_action", "delete_post_action", ]