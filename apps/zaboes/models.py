import uuid

from django.apps import apps as django_apps
from django.conf import settings
from django.db import models
from apps.users.models import ZaboUser

class Zabo(models.Model):
    CATEGORY = (
        ('R', 'Recruting'),
        ('P', 'Performance'),
        ('C', 'Competition'),
        ('F', 'Fair'),
        ('L','Lecture'),
        ('E', 'Exhibition'),
    )
    APPLY = (
        ('Z', 'Apply by zabo'),
        ('S', 'On-site reception'),
        ('E', 'External application')
    )
    PAYMENT_PLAN= (
        ('F', 'FREE'),
        ('Z', 'Paid by zabo'),
        ('A', 'Payment on account')
    )
    founder =  models.ForeignKey(
        ZaboUser, on_delete=models.CASCADE,
    )
    location = models.CharField(max_length=50)
    content = models.TextField(blank=True, null=True)
    category = models.CharField(
        max_length=1, choices=CATEGORY
    )
    apply = models.CharField(
        max_length=1, choices=APPLY
    )
    payment = models.CharField(
        max_length=1, choices=PAYMENT_PLAN
    )
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    limit = models.IntegerField(default = 1000)
    deadline = models.DateTimeField
    is_deleted = models.BooleanField(default = False)
    is_validated = models.BooleanField(default = False) # 관리자에게 승인받았는지 여부.


class Poster(models.Model):
    zabo  = models.ForeignKey(
        Zabo,
        on_delete=models.CASCADE,
    )
    image = models.FileField(upload_to='posters/%Y/%m/%d/')


class Timeslot(models.Model):
    zabo = models.ForeignKey(
        Zabo,
        on_delete=models.CASCADE,
    )
    start_time = models.DateTimeField
    end_time = models.DateTimeField
    is_main = models.BooleanField(default = False)

class Comment(models.Model):
    zabo = models.ForeignKey(
        Zabo,
        on_delete=models.CASCADE,
    )
    #author =
    content = models.CharField(max_length = 140)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    is_private = models.BooleanField(default = False)
    is_deleted = models.BooleanField(default = False)
    is_blocked = models.BooleanField(default = False)

class Recomment(models.Model):
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
    )
    #author =
    content = models.CharField(max_length = 140)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    is_private = models.BooleanField(default = False)
    is_deleted = models.BooleanField(default = False)
    is_blocked = models.BooleanField(default = False)

class Participate(models.Model):
    zabo = models.ForeignKey(
        Zabo,
        on_delete=models.CASCADE,
    )
    participants = models.OneToOneField(
        ZaboUser,
        on_delete= models.CASCADE,
    )
    is_paid = models.BooleanField(default = False)
    is_approved = models.BooleanField(default = False)
