from django.shortcuts import render
from rest_framework import viewsets
from api.users.serializers import ZabouserSerializer, ZabouserListSerializer
from apps.users.models import ZaboUser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    """
        This viewset automatically provides `list`, `create`, `retrieve`,
        `update` and `destroy` actions.

    """
    serializer_class = ZabouserSerializer
    queryset = ZaboUser.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('nickName', 'email')
    # 나중에 검색 결과 순서에 대해 이야기 해보아야 함
    ordering_fields = ('nickName', 'email', 'joined_date')

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = ZabouserListSerializer(page, many=True, context={
            'request': request,
        })

        if page is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)

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

    @action(methods=['post', 'delete'], detail=False)
    def unfollowOther(self, request):
        user = request.user
        nickname = request.data["nickname"]
        user.unfollow_others(nickname)
        return Response({'Message': 'You have successfully unfollow'}, status=status.HTTP_201_CREATED)
