from apps.notifications.models import ZaboReactionNotification, CommentReactionNotification
from apps.zaboes.models import Zabo, Comment, Recomment


class ReactionNotificatinoHelper():

    def __init__(self, From_user):
        self.From_user = From_user

    def notify_to_User(self, item, notifier):
        if isinstance(item, Zabo):
            self.notify_to_zaboUser(item, notifier)
        elif isinstance(item, Comment):
            self.notify_to_commentUser(item, notifier)

    def notify_to_zaboUser(self, zabo, notifier):
        user = zabo.founder
        if ZaboReactionNotification.objects.filter(zabo=zabo).exists():
            noti = ZaboReactionNotification.objects.filter(zabo=zabo)
            noti.followings.add(notifier)
            noti.save()
        else:
            content = zabo.content[:20]
            instance = ZaboReactionNotification(zabo=zabo, to=user, content=content)
            instance.followings.add(notifier)
            instance.save()

    def notify_to_commentUser(self, comment, notifier):
        user = comment.author
        if CommentReactionNotification.objects.filter(comment=comment).exists():
            noti = CommentReactionNotification.objects.filter(comment=comment)
            noti.followings.add(notifier)
            noti.save()
        else:
            content = comment.content[:20]
            instance = CommentReactionNotification(comment=comment, to=user, content=content)
            instance.followings.add(notifier)
            instance.save()

