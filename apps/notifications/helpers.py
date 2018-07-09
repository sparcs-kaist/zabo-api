from apps.notifications.models import ZaboReactionNotification, CommentReactionNotification, ZabpFollowingNotification
from apps.zaboes.models import Zabo, Comment, Recomment


class ReactionNotificatinoHelper():

    def __init__(self, notifier):
        self.notifier = notifier

    def notify_to_User(self, item):
        if isinstance(item, Zabo):
            self.notify_to_zaboUser(item, )
        elif isinstance(item, Comment):
            self.notify_to_commentUser(item)

    def notify_to_zaboUser(self, zabo):
        user = zabo.founder
        if ZaboReactionNotification.objects.filter(zabo=zabo).exists():
            noti = ZaboReactionNotification.objects.filter(zabo=zabo)
            noti.followings.add(self.notifier)
            noti.save()
        else:
            content = zabo.content[:20]
            instance = ZaboReactionNotification(zabo=zabo, to=user, content=content)
            instance.reactors.add(self.notifier)
            instance.save()

    def notify_to_commentUser(self, comment, notifier):
        user = comment.author
        if CommentReactionNotification.objects.filter(comment=comment).exists():
            noti = CommentReactionNotification.objects.filter(comment=comment)
            noti.reactors.add(self.notifier)
            noti.save()
        else:
            content = comment.content[:20]
            instance = CommentReactionNotification(comment=comment, to=user, content=content)
            instance.reactors.add(self.notifier)
            instance.save()


class FollowingNotificatinoHelper():

    def __init__(self, notifier):
        self.notifier = notifier

    def notify_to_User(self, item):
        if isinstance(item, Zabo):
            self.notify_to_zaboUser(item)

    def notify_to_zaboUser(self, zabo):
        user = zabo.founder
        content = zabo.content[:20]
        instance = ZaboReactionNotification(zabo=zabo, to=user, content=content, following=self.notifier)
        instance.save()
