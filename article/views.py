from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from django.db.models import Q
from .models import Article, ArticleComment, ArticleVote
from .serializers import ArticleSerializer, ArticleCommentSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from account.models import TopicTag


#list articles
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def articleListView(request):
    query = request.query_params.get('q')
    if query is None:
        query = ''
    articles = Article.objects.filter(Q(content__icontains=query) | Q(title__icontains=query)).order_by("-created")
    paginator = PageNumberPagination()
    paginator.page_size = 10
    result_page = paginator.paginate_queryset(articles, request)
    serializer = ArticleSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


#article detail view
@api_view(['GET'])
def articleDetailView(request, pk):
    try:
        article = Article.objects.get(id=pk)
        serializer = ArticleSerializer(article, many=False)
        return Response(serializer.data)
    except Exception as e:
        return Response({'details': f"{e}"}, status=status.HTTP_204_NO_CONTENT)
