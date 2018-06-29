from django.contrib import admin

from apps.zaboes.models import Zabo, Comment, Poster, Recomment, Timeslot, Participate, Like

# Register your models here.

admin.site.register(Zabo)
admin.site.register(Comment)
admin.site.register(Poster)
admin.site.register(Recomment)
admin.site.register(Timeslot)
admin.site.register(Participate)
admin.site.register(Like)
