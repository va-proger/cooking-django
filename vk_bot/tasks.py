from celery import shared_task
from .services import VKService
from blog.models import Post  # Предполагается, что модель постов блога уже существует

@shared_task
def auto_post_to_vk():
    # Постинг из Django в VK
    last_post = Post.objects.filter(posted_to_vk=False).last()
    if last_post:
        vk = VKService()
        vk.post_to_group(last_post.content)
        last_post.posted_to_vk = True
        last_post.save()

@shared_task
def import_vk_posts():
    vk = VKService()
    posts = vk.get_latest_posts(count=5)

    for post in posts:
        if not Post.objects.filter(vk_post_id=post["id"]).exists():
            Post.objects.create(
                title="Импортировано из VK",
                content=post["text"],
                vk_post_id=post["id"],
                posted_to_vk=True
            )