from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Feed
from account.serializers import UserProfileSerializer, UserSerializer


class FeedSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    parent_feed = serializers.SerializerMethodField(read_only=True)
    up_voters = serializers.SerializerMethodField(read_only=True)
    down_voters = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Feed
        fields = '__all__'

    def get_user(self, obj):
        user = obj.user.userprofile
        serializer = UserProfileSerializer(user, many=False)
        return serializer.data

    def get_parent_feed(self, obj):
        parent = obj.refeed
        if parent != None:
            serializer = FeedSerializer(parent, many=False)
            return serializer.data
        else:
            return None

    def get_up_voters(self, obj):
        voters = obj.votes.through.objects.filter(feed=obj, value='upvote').values_list('user', flat=True)
        voter_objects = obj.votes.filter(id__in=voters)
        serializer = UserSerializer(voter_objects, many=True)
        return serializer.data

    def get_down_voters(self, obj):
        voters = obj.votes.through.objects.filter(feed=obj, value='downvote').values_list('user', flat=True)
        voter_objects = obj.votes.filter(id__in=voters)
        serializer = UserSerializer(voter_objects, many=True)
        return serializer.data
