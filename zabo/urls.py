"""zabo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from rest_framework.schemas import get_schema_view
from django.contrib import admin
from rest_framework_swagger.views import get_swagger_view

from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

schema_view = get_schema_view(title='Pastebin API')
swagger_view = get_swagger_view(title="Pastebian API")

urlpatterns = (

                  url(r'^', include('api.urls')),
                  url(r'^api-token-auth/', obtain_jwt_token),
                  url(r'^api-token-refresh/', refresh_jwt_token),
                  url(r'^api-token-verify/', verify_jwt_token),
                  url(r'^schema/$', schema_view),
                  url(r'^swagger/$', swagger_view),
                  url(r'^admin/', admin.site.urls),
              ) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
