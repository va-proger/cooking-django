# Generated by Django 5.1.6 on 2025-03-11 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vproger", "0005_remove_post_detail_content_markdown"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="detail_content_markdown",
            field=models.TextField(
                blank=True,
                default="Скоро тут будет статья",
                verbose_name="Текст статьи - анонс",
            ),
        ),
    ]
