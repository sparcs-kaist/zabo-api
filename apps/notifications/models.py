from django.db import models
from apps.common.models import TimeStampedModel
from apps.users.models import ZaboUser
from apps.zaboes.models import Zabo, Comment, Recomment

# Create your models here.

class BaseNotification(TimeStampedModel):
    to = models.ForeignKey(
        ZaboUser, on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
    )
    content = models.CharField(blank=True, max_length=30)

    class Meta:
        abstract = True

class ReactionNotification(BaseNotification):
    reactors = models.ManyToManyField(ZaboUser)

    @property
    def reactors_count(self):
        return self.followings.count()

    class Meta:
        abstract = True

class ZaboReactionNotification(ReactionNotification):
    zabo = models.ForeignKey(
        Zabo, on_delete=models.CASCADE,
        related_name="zabo_reaction",

    )


class CommentReactionNotification(ReactionNotification):
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE,
        related_name="comment_reaction",
    )

class FollowingNotification(BaseNotification):
    following = models.ForeignKey(
        ZaboUser, on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
    )
    class Meta:
        abstract = True


class ZabpFollowingNotification(BaseNotification):
    zabo = models.ForeignKey(
        Zabo, on_delete=models.CASCADE,
        related_name="zabo_following",
    )

class AdminNotification(BaseNotification):
    pass
