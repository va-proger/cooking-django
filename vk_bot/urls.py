from django.urls import path, include
from . import views

urlpatterns = [
    path('callback/', views.vk_callback, name='vk_callback'),

]