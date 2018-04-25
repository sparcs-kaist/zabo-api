from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
#from api.zaboes.routers import zabo_router
from django.urls import path
from api.zaboes import views

zabo_router = DefaultRouter()
zabo_router.register(
    prefix=r'zaboes',
    viewset=views.ZaboViewSet,
)


urlpatterns = [
    url(r'^', include(zabo_router.urls)),
]
