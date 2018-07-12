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
        ordering = ['updated_time']


class ReactionNotification(BaseNotification):
    reactors = models.ManyToManyField(ZaboUser)

    @property
    def reactors_count(self):
        return self.reactors.count()

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
        related_name="%(app_label)s_%(class)s_related_following",
        related_query_name="%(app_label)s_%(class)ss_following",
    )

    class Meta:
        abstract = True


class ZaboFollowingNotification(FollowingNotification):
    zabo = models.ForeignKey(
        Zabo, on_delete=models.CASCADE,
        related_name="zabo_following",
    )


class SomeoneFollowingNotification(BaseNotification):
    following = models.ForeignKey(
        ZaboUser, on_delete=models.CASCADE
    )


class AdminNotification(BaseNotification):
    pass
