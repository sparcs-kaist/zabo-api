from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from api.users.views import UserViewSet

zabouser_router = DefaultRouter()

zabouser_router.register(
    prefix=r'users',
    viewset=UserViewSet,
)
