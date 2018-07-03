from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from api.users.routers import zabouser_router

urlpatterns = [
    url(r'^', include(zabouser_router.urls)),
]
