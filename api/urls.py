from django.conf.urls import include, url
from django.urls import path, re_path

from api.zaboes.routers import  *
urlpatterns = (

    url(r'^api/', include(router.urls)),
    path('users/', include('api.users.urls')),
)