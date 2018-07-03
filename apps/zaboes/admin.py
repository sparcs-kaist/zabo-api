from django.contrib import admin

from apps.zaboes.models import Zabo, Comment, Poster, Recomment, Timeslot, Participate


# Register your models here.
class ZaboAdmin(admin.ModelAdmin):
    list_per_page = 15
    list_display = (
        'id', 'title', 'content', 'founder', 'location', 'created_time',
    )
    search_fields = ('content',)
    fields = [Zabo.content, Zabo.APPLY]


class PosterAdmin(admin.ModelAdmin):
    list_per_page = 15
    list_display = (
        'id', 'zabo', 'image',
    )


admin.site.register(Zabo, ZaboAdmin)
admin.site.register(Comment)
admin.site.register(Poster, PosterAdmin)
admin.site.register(Recomment)
admin.site.register(Timeslot)
admin.site.register(Participate)
