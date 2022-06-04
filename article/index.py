from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register
from .models import Article


@register(Article)
class ArticleIndex(AlgoliaIndex):
    should_index = 'is_published'

    fields=[
        'title',
        'content',
        'user',
        'status',
        'tags'
    ]
    tags = 'topic_tags'

    # settings = {
    #     'searchableAttributes': ['title', 'content'],
    #     'attributesForFaceting': ['status'],
    # }
