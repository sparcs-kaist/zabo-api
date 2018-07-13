from django.conf.urls import include, url
from django.urls import path, re_path
from rest_framework_swagger.views import get_swagger_view
from api.users.routers import zabouser_router
from api.zaboes.routers import zabo_router
from api.notifications.routers import noti_router

swagger_view = get_swagger_view(title="Pastebian API")
urlpatterns = (

    url(r'^api/', include(zabo_router.urls)),
    url(r'^api/', include(zabouser_router.urls)),
    url(r'^api/', include(noti_router.urls)),
    url(r'^swagger/$', swagger_view),

)
