import vk_api
from django.conf import settings

class VKService:
    def __init__(self):
        self.session = vk_api.VkApi(token=settings.VK_USER_ACCESS_TOKEN)
        self.api = self.session.get_api()

    def post_to_group(self, text):
        response = self.api.wall.post(
            owner_id=f"-{settings.VK_GROUP_ID}",
            message=text,
            from_group=1
        )
        return response

    # Добавляем новый метод
    def delete_post(self, post_id):
        """Удаление поста из VK"""
        return self.api.wall.delete(
            owner_id=f"-{settings.VK_GROUP_ID}",
            post_id=post_id
        )