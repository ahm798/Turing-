import uuid

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone



class ModelQuerySet(models.QuerySet):
    def is_published(self):
        return self.filter(status='published')

    def search(self, query, user=None):
        lookup = Q(title__icontains=query) | Q(content__icontains=query)
        qs = self.is_published().filter(lookup)
        if user is not None:
            qs = qs.filter(owner__username=user)
        return qs


class ArticleManger(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return ModelQuerySet(self.model, using=self.db)

    def search(self, query, user=None):
        return self.get_queryset().is_published().search(query=query, user=user)




class Article(models.Model):
    STATUS_CHOICES = (('draft', 'Draft'), ('published', 'Published'))
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    title = models.CharField(max_length=500, default="untitled")
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    content = models.TextField()
    #
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    objects = ArticleManger()

    def is_published(self) -> bool:
        return self.status == 'published'

    #

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title



class ArticleComment(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user.username)


class ArticleVote(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    comment = models.ForeignKey(ArticleComment, on_delete=models.SET_NULL, null=True, blank=True)
    value = models.IntegerField(blank=True, null=True, default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.article} - count - {self.value}"
