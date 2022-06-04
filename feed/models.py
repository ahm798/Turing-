from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
import uuid


class Feed(models.Model):
    id = models.UUIDField(default=uuid.uuid4,  unique=True, primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="feeds")
    parent =models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    refeed = models.ForeignKey("self", on_delete=models.CASCADE, related_name='refeeds', null=True, blank=True)
    content = RichTextField(null=True, blank=True)
    image = models.ImageField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    vote_rank = models.IntegerField(blank=True, null=True, default=0)
    comment_count = models.IntegerField(blank=True, null=True, default=0)
    share_count = models.IntegerField(blank=True, null=True, default=0)
    votes = models.ManyToManyField(User, related_name='feed_user', blank=True, through='FeedVote')


    class Meta:
        ordering = ['-created']

    @property
    def shares(self):
        qs = self.refeeds.all()
        return qs

    @property
    def comments(self):
        qs = self.feed_set.all()
        return qs


class FeedVote(models.Model):
    CHOICES = (
        ('upvote', 'upvote'),
        ('downvote', 'downvote'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, null=True, blank=True)
    value = models.CharField(max_length=20, choices=CHOICES)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.user) + ' ' + str(self.value) + '"' + str(self.feed) + '"'