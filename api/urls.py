from django.conf.urls import include, url
from django.urls import path, re_path

urlpatterns = (
    path('zaboes/', include('api.zaboes.urls')),
)