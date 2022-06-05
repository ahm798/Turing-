from django.db import models
from django.contrib.auth.models import User
import uuid

from article.models import Article
from feed.models import Feed


class Notification(models.Model):
    CHOICES = (
        ('article', 'article'),
        ('feed', 'feed'),
        ('follow', 'follow'),
    )

    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    target = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    created = models.DateTimeField(auto_now_add=True)
    source = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    content = models.CharField(max_length=255)
    readed = models.BooleanField(default=False)
    notification_type = models.CharField(max_length=20, choices=CHOICES)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True, blank=True)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, null=True, blank=True)
    followed_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='followed_by')

    def __str__(self):
        return self.content