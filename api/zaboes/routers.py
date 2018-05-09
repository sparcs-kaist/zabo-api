from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from api.zaboes.views import ZaboViewSet, CommentViewSet, RecommentViewSet

router = SimpleRouter()

router.register(
    prefix=r'zaboes',
    viewset=ZaboViewSet,
)

router.register(
    prefix=r'comments',
    viewset=CommentViewSet,
)


router.register(
    prefix=r'recomments',
    viewset=RecommentViewSet,
)

