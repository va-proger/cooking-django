from django.apps import AppConfig


class CookingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "cooking"
    verbose_name = 'Блог'  # Новое название для отображения в админке