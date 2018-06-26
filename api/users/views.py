from django.shortcuts import render
from rest_framework import viewsets
from api.users import serializers
from apps.users.models import ZaboUser
from rest_framework.permissions import AllowAny, IsAuthenticated


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    """
        This viewset automatically provides `list`, `create`, `retrieve`,
        `update` and `destroy` actions.

    """
    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.ZabouserSerializer
    queryset = ZaboUser.objects.all()
