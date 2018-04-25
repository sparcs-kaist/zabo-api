from django.contrib import admin


from apps.users.models import ZaboUser
from apps.zaboes.models import Zabo, Comment, Poster, Recomment, Timeslot,Participate
# Register your models here.

admin.register(ZaboUser)
admin.register(Zabo)
admin.register(Comment)
admin.register(Poster)
admin.register(Recomment)
admin.register(Timeslot)
admin.register(Participate)