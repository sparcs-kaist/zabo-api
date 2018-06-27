from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter, SimpleRouter

from api.zaboes.views import ZaboViewSet, CommentViewSet, RecommentViewSet, PosterViewSet

zabo_router = SimpleRouter()

zabo_router.register(
    prefix=r'zaboes',
    viewset=ZaboViewSet,
)


zabo_router.register(
    prefix=r'posters',
    viewset=PosterViewSet,
)
  
zabo_router.register(
    prefix=r'comments',
    viewset=CommentViewSet,
)


zabo_router.register(
    prefix=r'recomments',
    viewset=RecommentViewSet,
)

