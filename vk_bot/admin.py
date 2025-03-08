import vk_api
from django.contrib import admin, messages
from django.http import HttpRequest
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from unfold.admin import ModelAdmin
from unfold.decorators import action

from conf import settings
from vk_bot.tasks import import_vk_posts
from vk_bot.models import VKPost
from vk_bot.services import VKService

csrf_protect_m = method_decorator(csrf_protect)


@admin.register(VKPost)
class VKPostAdmin(ModelAdmin):
    list_display = ('post_id', 'date', 'vk_group_id', 'from_django')
    actions_on_top = True    # Показывать действия над таблицей
    actions_on_bottom = True # Показывать действия под таблицей

    @action(description="📥 Импортировать посты из VK")
    def import_vk_posts_action(self, request, queryset):
        task = import_vk_posts.delay()
        messages.success(request, f"Импорт запущен! Задача ID: {task.id}")
        return redirect("admin:vk_bot_vkpost_changelist")

    @action(description="🚀 Опубликовать выбранное в VK")
    def post_to_vk_action(self, request, queryset):
        vk = VKService()
        count = 0
        for post in queryset:
            vk.post_to_group(post.text)
            count += 1
        messages.success(request, f"{count} постов отправлено в VK!")

    @action(description="❌ Удалить выбранное из VK")
    def delete_post_action(self, request, queryset):
        vk = VKService()
        count = 0
        for post in queryset:
            if post.post_id:
                try:
                    # Проверяем, существует ли пост
                    post_info = vk.api.wall.getById(posts=f"-{settings.VK_GROUP_ID}_{post.post_id}")
                    if post_info:
                        vk.delete_post(post.post_id)
                        count += 1
                    else:
                        messages.warning(request, f"Пост {post.post_id} не найден в группе {settings.VK_GROUP_ID}")
                except vk_api.exceptions.ApiError as e:
                    messages.error(request, f"Ошибка VK API при удалении поста {post.post_id}: {e}")
                except Exception as e:
                    messages.error(request, f"Ошибка при удалении поста {post.post_id}: {e}")
        messages.success(request, f"{count} постов удалено из VK!")

    # Регистрируем действия
    actions = ["import_vk_posts_action", "post_to_vk_action", "delete_post_action"]