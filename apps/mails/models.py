from django.db import models

from apps.common.models import TimeStampedModel

class ZaboMail(TimeStampedModel):
    sender_address =  models.CharField(blank=False, null=False, max_length=50 , default="")
    receivers_address= models.TextField(blank=True, null=True)
    subject = models.CharField(max_length=140, default="Title")
    message = models.TextField(blank=True, null=True)

    def set_receivers_address(self, mail_list):
        self.receivers_address = ':'.join(mail_list)

    def get_receivers_addresss(self):
        return self.receivers_address.split(':')

# Create your models here.
