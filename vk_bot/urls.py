from django.urls import path
from . import views

urlpatterns = [
    path('callback/', views.vk_callback, name='vk_callback'),
]