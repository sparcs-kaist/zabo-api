from .models import Zabo
from django.db import models
from django.utils import timezone
from django.http import Http404
import random


def get_random_zabo():
    max_id = Zabo.objects.filter(deadline__gt=timezone.now()).aggregate(max_id=models.Max("id"))['max_id']
    min_id = Zabo.objects.filter(deadline__gt=timezone.now()).aggregate(min_id=models.Min("id"))['min_id']
    if max_id is None or min_id is None:
        raise Http404('There is no zabo which is not finished')
    while True:
        pk = random.randint(min_id, max_id)
        zabo = Zabo.objects.filter(pk=pk).first()
        if zabo and (zabo.is_deleted == False) and (zabo.is_validated == False) and (zabo.is_finished == False):
            return zabo
