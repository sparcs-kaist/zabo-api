import uuid

from django.apps import apps as django_apps
from django.conf import settings
from django.db import models
from apps.users.models import ZaboUser
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.utils import timezone
from datetime import datetime


class Zabo(models.Model):
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

    founder = models.ForeignKey(
        ZaboUser, on_delete=models.CASCADE,
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
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField(editable=True, default=timezone.now())
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


class Comment(models.Model):
    zabo = models.ForeignKey(
        Zabo,
        related_name='comments',
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        ZaboUser, on_delete=models.CASCADE, default=None

    )
    content = models.CharField(max_length=140)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    is_private = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)


class Recomment(models.Model):
    comment = models.ForeignKey(
        Comment,
        related_name='recomments',
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        ZaboUser, on_delete=models.CASCADE,
        default=None
    )
    content = models.CharField(max_length=140)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    is_private = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)


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
