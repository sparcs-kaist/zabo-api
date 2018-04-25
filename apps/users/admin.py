from django.contrib import admin
from .models import ZaboUser
from apps.zaboes.models import Zabo, Comment, Poster, Recomment, Timeslot,Participate

# Register your models here.
admin.site.register(ZaboUser)