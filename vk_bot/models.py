from django.db import models


class VKPost(models.Model):
    post_id = models.CharField(max_length=255)
    text = models.TextField()
    date = models.DateTimeField()
    vk_group_id = models.CharField(max_length=50)
    from_django = models.BooleanField(default=False)

    def __str__(self):
        return f"Post {self.post_id}"