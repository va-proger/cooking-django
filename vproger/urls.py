from django.urls import path, include
from django.conf.urls.static import static
from .views import *
from django.conf import settings

handler404 = 'myapp.views.custom_404'
handler500 = 'myapp.views.custom_500'
# app_name = 'vproger'
urlpatterns = [
    path('markdownx/', include('markdownx.urls')),
    path("", index, name='index'),
    path('posts/', post_index),
    path('posts/<slug:category_slug>/', category_posts, name='category_posts'),  # Страница категории
    path('posts/<slug:category_slug>/<slug:post_slug>/', detail_post, name='detail_post'),  # Детальн
    path('tags/<slug:tag_slug>/', tag_posts, name='tag_posts'),  # Детальн
    path('search/', search_posts, name='search_posts'),
    path('filter-by-date/', filter_posts_by_date, name='filter_posts_by_date'),
    path('search-api/', search_api, name='search_api'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_ROOT, document_root=settings.STATIC_ROOT)
