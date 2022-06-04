def update_comment_counts(parent, action):
    if parent:
        if action == 'add':
            parent.comment_count += 1
        if action == 'delete':
            parent.comment_count -= 1
        parent.save()
        return update_comment_counts(parent.parent, action)

def update_refeed_counts(parent, action):

    if action == 'add':

        parent.share_count += 1

    if action == 'delete':
        parent.share_count -= 1

    parent.save()