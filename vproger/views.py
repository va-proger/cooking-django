from django.shortcuts import get_object_or_404, render
from .models import Category, Post, Tag
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
    return render(request, "vproger/index.html", context)

def detail_post(request, category_slug, post_slug):
    # Находим категорию по слагу
    category = get_object_or_404(Category, slug=category_slug)
    post = get_object_or_404(Post, slug=post_slug, category=category, is_published=True)
    context = {
        'post': post,
        'title': post.title,
    }

    return render(request, "vproger/post/detail.html", context)

def category_posts(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    posts = Post.objects.filter(category=category, is_published=True)
    context = {
        'category': category,
        'posts': posts,
        'title': f'Категория: {category.title}',
    }
    return render(request, 'vproger/category/category_posts.html', context)

def list_categories(request):
    categories = Category.objects.annotate(num_posts=Count('posts')).filter(num_posts__gt=0)
    tags = Tag.objects.annotate(num_posts=Count('posts')).filter(num_posts__gt=0)

    """ СТраница листинга"""
    context = {
        "title": "Главная страница",
        "categories": "categories",
    }
    return render(request, "vproger/list_news.html", context)

def dashboard_callback(request, context):
    context.update(
        {
            "custom_variable": "value",
        }
    )

    return context


def badge_callback_sidebar(request):
    return ""



