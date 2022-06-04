from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register
from .models import UserProfile

@register(UserProfile)
class AccountIndex(AlgoliaIndex):
    fields = [
        'username',
        'name'
    ]