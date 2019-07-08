from rest_framework.routers import DefaultRouter
from api.mails.views import ZaboMailViewSet

mail_router = DefaultRouter()

mail_router.register(
    prefix=r'mails',
    viewset=ZaboMailViewSet,
)
