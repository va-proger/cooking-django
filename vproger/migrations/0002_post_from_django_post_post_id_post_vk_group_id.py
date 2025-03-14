# Generated by Django 5.1.6 on 2025-03-07 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vproger", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="from_django",
            field=models.BooleanField(default=False, verbose_name="Из сайта"),
        ),
        migrations.AddField(
            model_name="post",
            name="post_id",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="post",
            name="vk_group_id",
            field=models.CharField(
                default="106003910",
                editable=False,
                max_length=50,
                verbose_name="vk_group_id группы",
            ),
        ),
    ]
