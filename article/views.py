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


#create article
@api_view(['POST'])
# @permission_classes((IsAuthenticated,))
def create_article(request):
    user = request.user
    print(user)
    data = request.data
    print(data)
    is_comment = data.get('isComment')
    if is_comment:
        article = Article.objects.get(id=data.get('postId'))
        comment = ArticleComment.objects.create(
            user=user,
            article=article,
            content=data.get('content'),
        )
        comment.save()
        serializer = ArticleCommentSerializer(comment, many=False)
        return Response(serializer.data)
    else:
        print(user)
        content = data.get('content')
        tags = data.get('tags')
        title = data.get('title')
        article = Article.objects.create(
            user=user,
            content=content,
            title=title,
        )
        if tags is not None:
            for tag_name in tags:
                tag_instance = TopicTag.objects.filter(name=tag_name).first()
                if not tag_instance:
                    tag_instance = TopicTag.objects.create(name=tag_name)
                article.tags.add(tag_instance)
        article.save()
    serializer = ArticleSerializer(article, many=False)
    return Response(serializer.data)