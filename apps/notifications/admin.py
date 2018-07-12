from django.contrib import admin
from apps.notifications.models import ZaboReactionNotification, CommentReactionNotification, ZaboFollowingNotification, \
    SomeoneFollowingNotification

# Register your models here.
admin.site.register(ZaboReactionNotification)
admin.site.register(CommentReactionNotification)
admin.site.register(ZaboFollowingNotification)
admin.site.register(SomeoneFollowingNotification)
