from django.urls import path, include
from django.conf.urls.static import static

from .views import *
from django.conf import settings
# app_name = 'vproger'
urlpatterns = [
    path('markdownx/', include('markdownx.urls')),
    path('<slug:category_slug>/<slug:post_slug>/', detail_post, name='detail_post'),
    path("", index),
    path('<slug:category_slug>/', category_posts, name='category_posts'),  # Страница категории
    path('<slug:category_slug>/<slug:post_slug>/', detail_post, name='detail_post'),  # Детальн


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_ROOT, document_root=settings.STATIC_ROOT)
