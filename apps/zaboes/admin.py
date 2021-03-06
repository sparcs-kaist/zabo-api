from django.contrib import admin

from apps.zaboes.models import Zabo, ZaboHistory, Comment, CommentHistory, Poster, Recomment, Timeslot, Participate, Like


# Register your models here.
class ZaboAdmin(admin.ModelAdmin):
    list_per_page = 15

    list_display = (
        'id', 'title', 'content', 'author', 'location', 'created_time',
    )
    search_fields = ('content',)

class TimeslotAdmin(admin.ModelAdmin):
    list_per_page = 15

    list_display = (
        'id', 'zabo', 'content',
    )
    search_fields = ('content',)

class PosterAdmin(admin.ModelAdmin):
    list_per_page = 15
    list_display = (
        'id', 'zabo', 'image',
    )


class LikeAdmin(admin.ModelAdmin):
    list_per_page = 15
    list_display = (
        'id', 'zabo', 'user',
    )


admin.site.register(Zabo, ZaboAdmin)
admin.site.register(ZaboHistory)
admin.site.register(Comment)
admin.site.register(Poster, PosterAdmin)
admin.site.register(Recomment)
admin.site.register(CommentHistory)
admin.site.register(Timeslot, TimeslotAdmin)
admin.site.register(Participate)
admin.site.register(Like, LikeAdmin)
