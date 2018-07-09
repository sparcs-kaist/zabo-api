from django.db import models
from apps.common.models import TimeStampedModel
from apps.users.models import ZaboUser
from apps.zaboes.models import Zabo, Comment, Recomment

# Create your models here.

class BaseNotification(TimeStampedModel):
    to = models.ForeignKey(
        ZaboUser, on_delete=models.CASCADE,
    )
    to_ink = models.URLField()
    content = models.CharField(blank=True)

    class Meta:
        abstract = True

class ReactionNotification(BaseNotification):
    reactors = models.ManyToManyField(ZaboUser)

    @property
    def reactors_count(self):
        return self.followings.count()

    class Meta:
        abstarct = True

class ZaboReactionNotification(ReactionNotification):
    zabo = models.ForeignKey(
        Zabo, on_delete=models.CASCADE,
    )


class CommentReactionNotification(ReactionNotification):
    comment = models.ForeignKey(
        Zabo, on_delete=models.CASCADE,
    )

class FollowingNotification(BaseNotification):
    following = models.ForeignKey(
        ZaboUser, on_delete=models.CASCADE,
    )
    class Meta:
        abstarct = True


class ZabpFollowingNotification(BaseNotification):
    zabo = models.ForeignKey(
        Zabo, on_delete=models.CASCADE,
    )

class AdminNotification(BaseNotification):
    pass
