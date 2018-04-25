from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from api.zaboes.views import ZaboViewSet

zabo_router = SimpleRouter()
zabo_router.register(r'zaboes', ZaboViewSet, base_name="zabo")