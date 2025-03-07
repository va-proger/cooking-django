from django.shortcuts import render
from .models import Category, Post
from django.conf import settings
from django.db.models import Count

def index(request):
    """Главная страница"""
    posts = Post.objects.filter(is_published=True)[:8]
    # Получаем категории, у которых есть хотя бы одна статья
    categories = Category.objects.annotate( num_posts=Count('posts')).filter( num_posts__gt=0)
    context = {
        "title": "Главная страница",
        "posts": posts,
        "categories": categories,
        "SITE_HEADER": settings.UNFOLD["SITE_HEADER"]
    }
    return render(request, "blog/index.html", context)


def dashboard_callback(request, context):
    context.update(
        {
            "custom_variable": "value",
        }
    )

    return context


def badge_callback_sidebar(request):
    return ""



