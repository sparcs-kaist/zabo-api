from django.db import models
from apps.common.models import TimeStampedModel
from apps.users.models import ZaboUser
from apps.zaboes.models import Zabo, Comment, Recomment


# Create your models here.

#Base model for notications model
class BaseNotification(TimeStampedModel):
    to = models.ForeignKey(
        ZaboUser, on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
    )
    content = models.CharField(blank=True, max_length=30)

    class Meta:
        abstract = True
        ordering = ['updated_time']

#base modle for reaction noti model
class ReactionNotification(BaseNotification):
    reactors = models.ManyToManyField(ZaboUser) # who react to someone.

    @property
    def reactors_count(self):
        return self.reactors.count()

    class Meta:
        abstract = True

#reaction to zabo
# 1. comment to zabo
# 2. like to zabo
class ZaboReactionNotification(ReactionNotification):
    zabo = models.ForeignKey(
        Zabo, on_delete=models.CASCADE,
        related_name="zabo_reaction",

    )
#reaction to zabo
# 1. recomment to comment
# 2.
class CommentReactionNotification(ReactionNotification):
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE,
        related_name="comment_reaction",
    )

#base modle for following noti model
class FollowingNotification(BaseNotification):
    following = models.ForeignKey(
        ZaboUser, on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_related_following",
        related_query_name="%(app_label)s_%(class)ss_following",
    )

    class Meta:
        abstract = True

#followings do something
# 1. add zabo
# 2.
class ZaboFollowingNotification(FollowingNotification):
    zabo = models.ForeignKey(
        Zabo, on_delete=models.CASCADE,
        related_name="zabo_following",
    )

#Someone follows
class SomeoneFollowingNotification(BaseNotification):
    following = models.ForeignKey(
        ZaboUser, on_delete=models.CASCADE
    )


class AdminNotification(BaseNotification):
    pass
