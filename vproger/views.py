from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.conf import settings
from django.db.models import Count
from django.core.cache import cache  # Кеширование
from django.views.decorators.cache import cache_page  # Декоратор кеширования
from .models import Category, Post, Tag
from django.utils.text import slugify
from transliterate import translit
from Levenshtein import distance as levenshtein_distance
from django.db.models import Q
import re


def get_common_context():
    """Получение категорий и тегов с кешированием"""
    cache_key = "common_context"
    context = cache.get(cache_key)

    if not context:
        context = {
            "categories": Category.objects.annotate(num_posts=Count('posts')).filter(num_posts__gt=0),
            "tags": Tag.objects.annotate(num_posts=Count('posts')).filter(num_posts__gt=0),
            "SITE_HEADER": settings.UNFOLD.get("SITE_HEADER", "Сайт"),
        }
        cache.set(cache_key, context, 1800)  # 30 минут

    return context

def cached_queryset(key, queryset, timeout=600):
    """Утилита кеширования запросов"""
    data = cache.get(key)
    if not data:
        data = queryset
        cache.set(key, data, timeout)
    return data

@cache_page(3600)  # 1 час
def menu_view(request):
    """Генерация меню с кешированием"""
    common_context = get_common_context()
    menu = [
        {"title": "Посты", "url": "/posts/", "sub": common_context["categories"]},
        {"title": "Проекты", "url": "/projects/"},
        {"title": "Галерея", "url": "/gallery/"},
        {"title": "Обо мне", "url": "/about/"},
    ]
    return render(request, "menu.html", {"menu": menu})

@cache_page(3600)
def index(request):
    """Главная страница"""
    context = get_common_context()
    posts = cached_queryset("index_posts", Post.objects.filter(is_published=True)[:8])
    context.update({"title": "Главная страница", "posts": posts})
    return render(request, "vproger/index.html", context)

@cache_page(600)  # 10 минут
def post_index(request):
    """Список постов"""
    context = get_common_context()
    cache_key = "post_index"
    posts = cache.get(cache_key)

    if not posts:
        posts = Post.objects.filter(is_published=True)
        cache.set(cache_key, posts, 600)  # 10 минут

    context.update({"title": "Список постов", "posts": posts})
    return render(request, "vproger/index.html", context)

# @cache_page(3600)  # 1 час
def detail_post(request, category_slug, post_slug):
    """Детальная страница поста с кешированием"""
    cache_key = f"post_{category_slug}_{post_slug}"
    post = cache.get(cache_key)

    if not post:
        post = get_object_or_404(Post, slug=post_slug, category__slug=category_slug, is_published=True)
        cache.set(cache_key, post, 3600)  # 1 час

    context = get_common_context()
    context.update({"title": post.title, "post": post})
    return render(request, "vproger/post/detail.html", context)

@cache_page(900)
def category_posts(request, category_slug):
    """Посты по категории"""
    context = get_common_context()
    category = cached_queryset(f"category_{category_slug}", get_object_or_404(Category, slug=category_slug))
    posts = Post.objects.filter(category=category, is_published=True)
    context.update({
        "title": f'Категория: {category.title}',
        "category": category,
        "posts": posts,
    })
    return render(request, "vproger/category/category_posts.html", context)

@cache_page(900)  # 15 минут
def tag_posts(request, tag_slug):
    """Посты по тегу с кешированием"""
    cache_key = f"tag_{tag_slug}"
    tag = cache.get(cache_key)

    if not tag:
        tag = get_object_or_404(Tag, slug=tag_slug)
        cache.set(cache_key, tag, 900)  # 15 минут

    context = get_common_context()
    context.update({
        "title": f'Тег: {tag.name}',
        "tag": tag,
        "posts": tag.posts.filter(is_published=True),
    })
    return render(request, "vproger/tags_posts.html", context)

@cache_page(1800)  # 30 минут
def list_categories(request):
    """Список категорий с кешированием"""
    context = get_common_context()
    context.update({"title": "Категории"})
    return render(request, "vproger/list_news.html", context)


def custom_404(request, exception):
    """Кастомная страница 404"""
    return render(request, 'errors/404.html', status=404)


def search_posts(request):
    """Поиск постов по ключевым словам, включая исправление опечаток и корректировку раскладки"""
    query = request.GET.get('s', '').strip()
    posts = Post.objects.none()  # Изначально пустой queryset

    if query:
        def correct_keyboard_layout(text):
            """Коррекция раскладки клавиатуры"""
            ru_to_en = str.maketrans("йцукенгшщзхъфывапролджэячсмитьбю", "qwertyuiop[]asdfghjkl;'zxcvbnm,.")
            en_to_ru = str.maketrans("qwertyuiop[]asdfghjkl;'zxcvbnm,.", "йцукенгшщзхъфывапролджэячсмитьбю")
            return [text.translate(ru_to_en), text.translate(en_to_ru)]

        def levenshtein_distance(s1, s2):
            """Вычисление расстояния Левенштейна между двумя строками"""
            if len(s1) < len(s2):
                return levenshtein_distance(s2, s1)
            if len(s2) == 0:
                return len(s1)

            previous_row = range(len(s2) + 1)
            for i, c1 in enumerate(s1):
                current_row = [i + 1]
                for j, c2 in enumerate(s2):
                    insertions = previous_row[j + 1] + 1
                    deletions = current_row[j] + 1
                    substitutions = previous_row[j] + (c1 != c2)
                    current_row.append(min(insertions, deletions, substitutions))
                previous_row = current_row

            return previous_row[-1]

        def find_similar_words(query_word, fields, max_distance=0.2):
            """Поиск похожих слов с использованием расстояния Левенштейна"""
            if len(query_word) <= 2:  # Слишком короткие слова пропускаем
                return []

            similar_posts = []
            possible_posts = Post.objects.filter(is_published=True)  # Только опубликованные посты

            # Проверка расстояния Левенштейна для заданных полей
            for post in possible_posts:
                for field in fields:
                    post_text = getattr(post, field, "")
                    if post_text:
                        # Разбиваем текст поста на отдельные слова
                        post_words = set(word.lower() for word in re.findall(r'\w+', post_text.lower()))

                        # Проверяем каждое слово в тексте
                        for post_word in post_words:
                            if len(post_word) > 2:  # Игнорируем слишком короткие слова
                                distance = levenshtein_distance(query_word.lower(), post_word)
                                threshold = max(1, len(query_word) * max_distance)  # Минимум 1 символ
                                if distance <= threshold:
                                    similar_posts.append(post)
                                    break  # Достаточно одного совпадения для поста

            return similar_posts

        # Импортируем необходимые модули
        import re
        from transliterate import translit

        # Возможные варианты запроса: раскладка, транслитерация
        possible_queries = [query] + correct_keyboard_layout(query)

        # Добавляем транслитерацию только если функция доступна
        try:
            possible_queries.extend([
                translit(query, 'ru', reversed=True),  # Латиница -> Кириллица
                translit(query, 'ru')  # Кириллица -> Латиница
            ])
        except:
            pass  # Если транслитерация не работает, просто пропускаем

        # Уникальные запросы
        possible_queries = list(set(filter(None, possible_queries)))

        # Поиск постов по возможным вариантам
        for alternative_query in possible_queries:
            posts |= Post.objects.filter(
                Q(title__icontains=alternative_query) |
                Q(detail_content_markdown__icontains=alternative_query) |
                Q(detail_content__icontains=alternative_query)
            )

        # Разбиваем запрос на отдельные слова для поиска похожих
        query_words = re.findall(r'\w+', " ".join(possible_queries))

        # Поиск близких слов с учётом расстояния Левенштейна
        similar_posts = []
        for query_word in query_words:
            similar_posts += find_similar_words(
                query_word,
                ['title', 'detail_content_markdown', 'detail_content'],
                max_distance=0.3  # Увеличиваем порог для лучших результатов
            )

        # Добавляем найденные посты и убираем дубликаты
        posts = posts | Post.objects.filter(pk__in=[post.pk for post in similar_posts])

    return render(request, 'search_results.html', {
        'query': query,
        'posts': posts.distinct(),
        'title': 'Результаты поиска',
        "SITE_HEADER": settings.UNFOLD.get("SITE_HEADER", "Сайт"),
    })

def filter_posts_by_date(request):
    """Фильтрация постов по дате"""
    from_date = request.GET.get('from')
    to_date = request.GET.get('to')
    posts = Post.objects.filter(is_published=True)

    if from_date:
        posts = posts.filter(created_at__gte=from_date)
    if to_date:
        posts = posts.filter(created_at__lte=to_date)

    return render(request, 'filter_results.html', {
        'posts': posts,
        'title': 'Фильтр по дате'
    })


def search_api(request):
    """AJAX API для поиска постов"""
    query = request.GET.get('s', '').strip()
    results = []

    if query and len(query) >= 2:
        def correct_keyboard_layout(text):
            """Коррекция раскладки клавиатуры"""
            ru_to_en = str.maketrans("йцукенгшщзхъфывапролджэячсмитьбю", "qwertyuiop[]asdfghjkl;'zxcvbnm,.")
            en_to_ru = str.maketrans("qwertyuiop[]asdfghjkl;'zxcvbnm,.", "йцукенгшщзхъфывапролджэячсмитьбю")
            return [text.translate(ru_to_en), text.translate(en_to_ru)]

        def find_similar_words(query_word, fields, max_distance=0.3):
            """Поиск похожих слов с использованием расстояния Левенштейна"""
            if len(query_word) <= 2:  # Слишком короткие слова пропускаем
                return []

            similar_posts = []
            possible_posts = Post.objects.filter(is_published=True)  # Только опубликованные посты

            # Проверка расстояния Левенштейна для заданных полей
            for post in possible_posts:
                for field in fields:
                    post_text = getattr(post, field, "")
                    if post_text:
                        # Разбиваем текст поста на отдельные слова
                        post_words = set(word.lower() for word in re.findall(r'\w+', post_text.lower()))

                        # Проверяем каждое слово в тексте
                        for post_word in post_words:
                            if len(post_word) > 2:  # Игнорируем слишком короткие слова
                                distance = levenshtein_distance(query_word.lower(), post_word)
                                threshold = max(1, len(query_word) * max_distance)  # Минимум 1 символ
                                if distance <= threshold:
                                    similar_posts.append(post)
                                    break  # Достаточно одного совпадения для поста

            return similar_posts

        # Возможные варианты запроса: раскладка, транслитерация
        possible_queries = [query] + correct_keyboard_layout(query)

        # Добавляем транслитерацию если возможно
        try:
            from transliterate import translit
            possible_queries.extend([
                translit(query, 'ru', reversed=True),  # Латиница -> Кириллица
                translit(query, 'ru')  # Кириллица -> Латиница
            ])
        except ImportError:
            pass  # Если модуль не установлен, просто пропускаем

        # Уникальные запросы
        possible_queries = list(set(filter(None, possible_queries)))

        # Поиск постов по возможным вариантам
        posts = Post.objects.none()
        for alternative_query in possible_queries:
            posts |= Post.objects.filter(
                Q(title__icontains=alternative_query) |
                Q(detail_content_markdown__icontains=alternative_query) |
                Q(detail_content__icontains=alternative_query)
            ).filter(is_published=True)

        # Разбиваем запрос на отдельные слова для поиска похожих
        query_words = re.findall(r'\w+', " ".join(possible_queries))

        # Поиск близких слов с учётом расстояния Левенштейна
        similar_posts = []
        for query_word in query_words:
            similar_posts += find_similar_words(
                query_word,
                ['title', 'detail_content_markdown', 'detail_content'],
                max_distance=0.3  # Порог для лучших результатов
            )

        # Добавляем найденные посты и убираем дубликаты
        posts = posts | Post.objects.filter(pk__in=[post.pk for post in similar_posts])
        posts = posts.distinct()[:10]  # Ограничиваем количество результатов

        # Формируем результаты в нужном формате
        for post in posts:
            post_data = {
                'id': post.id,
                'title': post.title,
                'url': post.get_absolute_url(),  # Используем get_absolute_url вместо slug
                'image': post.preview_image.url if hasattr(post, 'preview_image') and post.preview_image else None,  # Анонс-картинка
            }

            # Добавляем содержимое, если оно доступно
            if hasattr(post, 'detail_content') and post.detail_content:
                post_data['detail_content'] = post.detail_content[:50]

            if hasattr(post, 'detail_content_markdown') and post.detail_content_markdown:
                post_data['detail_content_markdown'] = post.detail_content_markdown[:50]

            if hasattr(post, 'published_at'):
                post_data['published_at'] = post.published_at.isoformat() if post.published_at else None

            results.append(post_data)

    return JsonResponse({'results': results})