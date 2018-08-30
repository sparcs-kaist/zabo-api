import uuid

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from apps.users.models import ZaboUser
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.utils import timezone
from datetime import datetime
from apps.common.models import TimeStampedModel, HavingAuthorModel


class Zabo(TimeStampedModel, HavingAuthorModel):
    CATEGORY = (
        ('R', 'Recruting'),
        ('P', 'Performance'),
        ('C', 'Competition'),
        ('F', 'Fair'),
        ('L', 'Lecture'),
        ('E', 'Exhibition'),
    )
    APPLY = (
        ('Z', 'Apply by zabo'),
        ('S', 'On-site reception'),
        ('E', 'External application')
    )
    PAYMENT_PLAN = (
        ('F', 'FREE'),
        ('Z', 'Paid by zabo'),
        ('A', 'Payment on account')
    )


    title = models.CharField(max_length=50, default="Title")
    location = models.CharField(max_length=50)
    link_url = models.CharField(max_length=200, blank=True) #naming to avoid collision to hyperlinkseralizer url field.
    content = models.TextField(blank=True, null=True)
    category = models.CharField(
        max_length=1, choices=CATEGORY,
    )
    apply = models.CharField(
        max_length=1, choices=APPLY
    )
    payment = models.CharField(
        max_length=1, choices=PAYMENT_PLAN
    )
    deadline = models.DateTimeField(editable=True, default=timezone.now)
    is_deleted = models.BooleanField(default=False)
    is_validated = models.BooleanField(default=False)  # 관리자에게 승인받았는지 여부.

    @property
    def like_count(self):
        return self.likes.all().count()

    @property
    def time_left(self):
        current = timezone.now()
        diff = self.deadline - current
        return diff
        return datetime.timedelta(diff).total_seconds()

    @property
    def is_finished(self):
        current = timezone.now()
        diff = self.deadline - current
        if str(diff)[0] == '-':
            return True
        else:
            return False


class ZaboHistory(models.Model):
    zabo = models.ForeignKey(
        Zabo,
        related_name='history',
        on_delete=models.CASCADE
    )
    created_date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

class Poster(models.Model):
    zabo = models.ForeignKey(
        Zabo,
        related_name='posters',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    image = models.FileField(upload_to='posters/')
    image_thumbnail = ImageSpecField(source='image',
                                     processors=[ResizeToFill(600, 800)],
                                     format='JPEG',
                                     options={'quality': 60},
                                     )


class Timeslot(models.Model):
    zabo = models.ForeignKey(
        Zabo,
        related_name='timeslots',
        on_delete=models.CASCADE,
    )
    content = models.CharField(max_length=50, default=None)
    start_time = models.DateTimeField(default=None)
    end_time = models.DateTimeField(default=None)


class Comment(TimeStampedModel, HavingAuthorModel):
    zabo = models.ForeignKey(
        Zabo,
        related_name='comments',
        on_delete=models.CASCADE,
    )
    content = models.CharField(max_length=140)
    is_private = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)


class Recomment(TimeStampedModel, HavingAuthorModel):
    comment = models.ForeignKey(
        Comment,
        related_name='recomments',
        on_delete=models.CASCADE,
    )
    content = models.CharField(max_length=140)
    is_private = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)

class CommentHistory(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=140)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    comment = GenericForeignKey('content_type', 'object_id')

class Participate(models.Model):
    zabo = models.ForeignKey(
        Zabo,
        on_delete=models.CASCADE,
    )
    participants = models.OneToOneField(
        ZaboUser,
        on_delete=models.CASCADE,
    )
    is_paid = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)


class Like(models.Model):
    zabo = models.ForeignKey(
        Zabo,
        on_delete=models.CASCADE,
        related_name="likes",
    )
    user = models.ForeignKey(
        ZaboUser,
        on_delete=models.CASCADE,
        default=None,
    )
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('zabo', 'user')
