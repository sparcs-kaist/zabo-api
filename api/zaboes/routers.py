from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from api.zaboes.views import ZaboViewSet, PosterViewSet

zabo_router = DefaultRouter()
zabo_router.register(
    prefix=r'',
    viewset=ZaboViewSet,
)

poster_router = DefaultRouter()
poster_router.register(
    prefix=r'',
    viewset=PosterViewSet,
)

