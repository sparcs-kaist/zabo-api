from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from api.zaboes.views import ZaboViewSet, CommentViewSet

zabo_router = DefaultRouter()
zabo_router.register(
    prefix=r'',
    viewset=ZaboViewSet,
)
comment_router = DefaultRouter()
comment_router.register(
    prefix=r'',
    viewset=CommentViewSet,
)