from django.conf.urls import include, url
from django.urls import path, re_path
from rest_framework_swagger.views import get_swagger_view

swagger_view = get_swagger_view(title="Pastebian API")


from api.zaboes.routers import  *
urlpatterns = (

    url(r'^api/', include(router.urls)),
    path('users/', include('api.users.urls')),
    url(r'^swagger/$', swagger_view),

)