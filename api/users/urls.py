from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    url(r'^',
        include(router.urls)),
]
