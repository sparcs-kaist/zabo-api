from django.shortcuts import render
from rest_framework import viewsets
from api.users import serializers
from apps.users.models import ZaboUser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    """
        This viewset automatically provides `list`, `create`, `retrieve`,
        `update` and `destroy` actions.

    """
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ZabouserSerializer
    queryset = ZaboUser.objects.all()

    @action(methods=['get'], detail=False)
    def myInfo(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(methods=["post"], detail=False)
    def followOther(self, request):
        user = request.user
        nickname = request.data["nickname"]
        user.follow_others(nickname)
        return Response({'Message': 'You have successfully follow'}, status=status.HTTP_201_CREATED)
