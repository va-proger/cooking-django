from django.shortcuts import render
from .models import Category, Post

def index(request):
    ''' Главная страница'''
    posts = Post.objects.all()
    categories = Category.objects.all()
    context = {
        'title': 'Главная страница',
        'posts': posts,
        'categories': categories,
    }
    return render(request, 'cooking/index.html', context)

def dashboard_callback(request, context):
    context.update({
        "custom_variable": "value",
    })

    return context

def badge_callback_sidebar(request):
    return ''