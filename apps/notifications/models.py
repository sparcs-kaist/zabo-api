from django.db import models
from apps.common.models import TimeStampedModel
from apps.users.models import ZaboUser

# Create your models here.

class BaseNotification(TimeStampedModel):
    to = models.ForeignKey(
        ZaboUser, on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True

class FollowingNotification(BaseNotification):
    following = models.ForeignKey(
        ZaboUser, on_delete=models.CASCADE,
    )

