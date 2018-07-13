from rest_framework.routers import DefaultRouter
from api.notifications.views import NotificationViewSet

noti_router = DefaultRouter()

noti_router.register(
    prefix=r'notifications',
    viewset=NotificationViewSet
)