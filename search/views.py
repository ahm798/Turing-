from rest_framework import generics
from rest_framework.response import Response
from article.serializers import ArticleSerializer
from article.models import Article
from . import client
#
#
# class SearchOldArticleListView(generics.ListAPIView):
#     serializer_class = ArticleSerializerDetial
#     queryset = Article.objects.all()
#
#     def get_queryset(self, *args, **kwargs):
#         qs = super().get_queryset()
#         q = self.request.GET.get('q')
#         user = None
#         result = Article.objects.none()
#         if q is not None:
#             if self.request.user.is_authenticated:
#                 user=self.request.user.username
#             result = qs.search(query=q, user=user)
#         return result
#
#
class SearchApiView(generics.GenericAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get(self, request, *args, **kwargs):
        tag= self.request.GET.get('tag') or None
        query = request.GET.get('q')
        if not query:
            return Response('', status=400)
        result = client.perform_search(query, tags=tag)
        return Response(result)
