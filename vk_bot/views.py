from datetime import datetime
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import VKPost


@csrf_exempt
def vk_callback(request):
    data = json.loads(request.body)

    # Проверка секретного ключа
    if data.get('secret') != settings.VK_SECRET_KEY:
        return HttpResponse('invalid secret', status=403)

    # Подтверждение сервера
    if data.get('type') == 'confirmation':
        return HttpResponse(settings.VK_CONFIRMATION_CODE)

    # Обработка нового поста
    if data.get('type') == 'wall_post_new':
        post_data = data['object']
        VKPost.objects.create(
            post_id=post_data['id'],
            text=post_data['text'],
            date=datetime.fromtimestamp(post_data['date']),
            vk_group_id=post_data['owner_id']
        )

    return HttpResponse('ok')
