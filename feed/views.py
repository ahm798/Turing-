from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Feed, FeedVote
from .serializers import FeedSerializer


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def feeds(request):
    user = request.user
    following = user.following.select_related('user')

    following = user.following.all()

    ids = []
    ids = [i.user.id for i in following]
    ids.append(user.id)
    print('IDS:', ids)
    feeds = list(Feed.objects.filter(parent=None, user__id__in=ids).order_by("-created"))[0:5]
    recentFeeds = Feed.objects.filter(Q(parent=None) & Q(vote_rank__gte=0) & Q(refeed=None)).order_by("-created")[0:5]
    topFeeds = Feed.objects.filter(Q(parent=None)).order_by("-vote_rank", "-created")
    index = 0
    for feed in recentFeeds:
        if feed not in feeds:
            feeds.insert(index, feed)
            index += 1
    for feed in topFeeds:
        if feed not in feeds:
            feeds.append(feed)

    paginator = PageNumberPagination()
    paginator.page_size = 10
    result_page = paginator.paginate_queryset(feeds, request)
    serializer = FeedSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def feedDetailView(request, pk):
    try:
        feed = Feed.objects.get(id=pk)
        serializer = FeedSerializer(feed, many=False)
        return Response(serializer.data)
    except:
        message = {
            'detail': 'Feed doesn\'t exist'
        }
        return Response(message, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def createFeedView(request):
    user = request.user
    data = request.data

    is_comment = data.get('isComment')
    if is_comment:
        parent = Feed.objects.get(id=data['postId'])
        feed = Feed.objects.create(
            parent=parent,
            user=user,
            content=data['content'],
        )
    else:
        feed = Feed.objects.create(
            user=user,
            content=data['content']
        )

    serializer = FeedSerializer(feed, many=False)
    return Response(serializer.data)


@api_view(['PATCH'])
@permission_classes((IsAuthenticated,))
def editFeedView(request, pk):
    user = request.user
    data = request.data

    try:
        feed = Feed.objects.get(id=pk)
        if user != feed.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            serializer = FeedSerializer(feed, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
    except Exception as e:
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def deleteFeedView(request, pk):
    user = request.user
    try:
        feed = Feed.objects.get(id=pk)
        if user != feed.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            feed.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({'details': f"{e}"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def feedCommentView(request, pk):
    feed = Feed.objects.get(id=pk)
    comments = feed.feed_set.all()
    serializer = FeedSerializer(comments, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def refeedView(request):
    user = request.user
    data = request.data
    original_feed = Feed.objects.get(id=data['id'])
    if original_feed.user == user:
        return Response({'detail': 'You can not refeed your own feed.'}, status=status.HTTP_403_FORBIDDEN)
    try:
        feed = Feed.objects.filter(
            refeed=original_feed,
            user=user,
        )
        if feed.exists():
            return Response({'detail': 'Already feeded'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            feed = Feed.objects.create(
                refeed=original_feed,
                user=user,
            )
        serializer = FeedSerializer(feed, many=False)
        return Response(serializer.data)
    except Exception as e:
        return Response({'detail': f'{e}'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def voteUpdateView(request):
    user = request.user
    data = request.data

    feed = Feed.objects.get(id=data['post_id'])
    vote, created = FeedVote.objects.get_or_create(feed=feed, user=user)

    if vote.value == data.get('value'):
        vote.delete()
    else:

        vote.value = data['value']
        vote.save()
    feed = Feed.objects.get(id=data['post_id'])
    serializer = FeedSerializer(feed, many=False)

    return Response(serializer.data)
