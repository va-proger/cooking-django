from django.urls import path
from django.conf.urls.static import static
from .views import *
from django.conf import settings

urlpatterns = [
    path("", index),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_ROOT, document_root=settings.STATIC_ROOT)
