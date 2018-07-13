from apps.notifications.models import ZaboReactionNotification, CommentReactionNotification, ZaboFollowingNotification, \
    SomeoneFollowingNotification
from apps.zaboes.models import Zabo, Comment, Recomment
from itertools import chain
from api.zaboes.serializers import ZaboUrlSerializer


class ReactionNotificatinoHelper():

    def __init__(self, notifier):
        self.notifier = notifier

    def notify_to_User(self, item):
        if isinstance(item, Zabo):
            self.notify_to_zaboUser(item)
        elif isinstance(item, Comment):
            self.notify_to_commentUser(item)

    def notify_to_zaboUser(self, zabo):
        user = zabo.founder
        if self.notifier == user:
            return

        if ZaboReactionNotification.objects.filter(zabo=zabo).exists():
            noti = ZaboReactionNotification.objects.filter(zabo=zabo)
            noti.reactors.add(self.notifier)
            noti.save()
        else:
            content = zabo.content[:20]
            instance = ZaboReactionNotification(zabo=zabo, to=user, content=content)
            instance.save()
            instance.reactors.add(self.notifier)
            instance.save()

    def notify_to_commentUser(self, comment):
        user = comment.author
        if self.notifier == user:
            return

        if CommentReactionNotification.objects.filter(comment=comment).exists():
            noti = CommentReactionNotification.objects.filter(comment=comment)
            noti.reactors.add(self.notifier)
            noti.save()
        else:
            content = comment.content[:20]
            instance = CommentReactionNotification(comment=comment, to=user, content=content)
            instance.save()
            instance.reactors.add(self.notifier)
            instance.save()

    def cancel_reaction(self, item):
        if isinstance(item, Zabo):
            noti = ZaboReactionNotification.objects.filter(zabo=item)
        elif isinstance(item, Comment):
            noti = CommentReactionNotification.objects.filter(comment=item)
        noti.followings.remove(self.notifier)
        noti.save()
        if noti.followings.count() <= 0:
            noti.delete()


class FollowingNotificatinoHelper():

    def __init__(self, notifier, to):
        self.notifier = notifier
        self.to = to

    def notify_to_User(self, item):
        if isinstance(item, Zabo):
            self.notify_to_zaboUser(item)

    def notify_to_zaboUser(self, zabo):
        content = zabo.content[:20]
        instance = ZaboFollowingNotification(zabo=zabo, to=self.to, content=content, following=self.notifier)
        instance.save()


class SomeoneFollowingNotificatinoHelper():

    def __init__(self, notifier, following):
        self.notifier = notifier
        self.following = following

    def notify_to_User(self):
        instance = SomeoneFollowingNotification(to=self.notifier, following=self.following)
        instance.save()


# get querysets from various noti models & combine them  & sort them by updated time
def get_sorted_noti_list_by_user(user):
    ZaboReactors = ZaboReactionNotification.objects.filter(to=user)
    CommentReactors = CommentReactionNotification.objects.filter(to=user)
    ZaboFollowings = ZaboFollowingNotification.objects.filter(to=user)
    SomeoneFollowings = SomeoneFollowingNotification.objects.filter(to=user)
    result_list = sorted(
        chain(ZaboReactors, CommentReactors, ZaboFollowings, SomeoneFollowings),
        key=lambda instance: instance.updated_time, reverse=True)
    return result_list


def convert_noti_list_to_queryset(request, noti_list):
    ret = []
    context = {"request": request}
    try:
        for noti in noti_list:
            ret_noti = {}
            if isinstance(noti, ZaboReactionNotification):
                serializer = ZaboUrlSerializer(noti.zabo, context=context)
                ret_noti["reactors_count"] = noti.reactors_count
                ret_noti["content"] = noti.content
                ret_noti["from"] = noti.reactors.first().nickName
                ret_noti["url"] = serializer.data["url"]
                ret_noti["type"] = "ZaboReaction"
            elif isinstance(noti, CommentReactionNotification):
                serializer = ZaboUrlSerializer(noti.comment.zabo, context=context)
                ret_noti["reactors_count"] = noti.reactors_count
                ret_noti["content"] = noti.content
                ret_noti["from"] = noti.reactors.first().nickName
                ret_noti["url"] = serializer.data["url"]
                ret_noti["type"] = "CommentReaction"
            elif isinstance(noti, ZaboFollowingNotification):
                serializer = ZaboUrlSerializer(noti.zabo, context=context)
                ret_noti["from"] = noti.following.nickName
                ret_noti["content"] = noti.content
                ret_noti["url"] = serializer.data["url"]
                ret_noti["type"] = "ZaboFollowing"
            elif isinstance(noti, SomeoneFollowingNotification):
                ret_noti["from"] = noti.following.nickName
                ret_noti["type"] = "SomeoneFollowing"
            else:
                print(noti, 'unexpected type notification')
                raise StopIteration
            ret_noti["updated_at"] = noti.updated_time
            ret.append(ret_noti)
        return ret
    except StopIteration:
        print("well stopped")
