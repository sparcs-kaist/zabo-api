from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from api.zaboes.routers import zabo_router, comment_router
from django.urls import path
from api.zaboes import views

urlpatterns = [
    url(r'^', include(zabo_router.urls)),
    url(r'comments/', include(comment_router.urls))

]
