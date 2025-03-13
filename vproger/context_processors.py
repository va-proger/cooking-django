from django.db.models import Count

from .models import SiteSettings, Category


def site_settings(request):
    return {
        'site_settings': SiteSettings.get_solo()
    }

def menu(request):
    post_categories = Category.objects.annotate(num_posts=Count('posts')).filter(num_posts__gt=0)

    return {
        "menu": [
            {"title": "Посты", "url": "/posts/", "sub": post_categories},
            {"title": "Проекты", "url": "/projects/", },
            # {"title": "Проекты", "url": "/projects/", "sub": project_categories},
            {"title": "Галерея", "url": "/gallery/"},
            {"title": "Обо мне", "url": "/about/"},
        ]
    }

