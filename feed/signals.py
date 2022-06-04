from django.db.models.signals import post_save, pre_save, post_delete
from .models import Feed, FeedVote
from .utils import update_comment_counts, update_refeed_counts


def update_mumble(sender, instance, created, **kwargs):
    if created and instance.parent:
        update_comment_counts(instance.parent, 'add')

    if instance.remumble:
        parent = instance.remumble
        update_refeed_counts(parent, 'add')


def delete_feed_comments(sender, instance, **kwargs):
    try:
        if instance.parent:
            update_comment_counts(instance.parent, 'delete')
    except Exception as e:
        print('feed associated with comment was deleted')
    try:
        if instance.refeed:
            update_refeed_counts(instance.refeed, 'delete')
    except Exception as e:
        print('refeed associated with comment was deleted')


post_save.connect(update_mumble, sender=Feed)
post_delete.connect(delete_feed_comments, sender=Feed)


def vote_updated(sender, instance, **kwargs):
    try:
        feed = instance.feed
        up_votes = len(feed.votes.through.objects.filter(feed=feed, value='upvote'))
        down_votes = len(feed.votes.through.objects.filter(feed=feed, value='downvote'))
        feed.vote_rank = (up_votes - down_votes)
        feed.save()
    except Exception as e:
        print('mumble the vote was associated with was already deleted')


post_save.connect(vote_updated, sender=FeedVote)
post_delete.connect(vote_updated, sender=FeedVote)
