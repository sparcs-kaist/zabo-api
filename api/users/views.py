from rest_framework import viewsets
from api.users.serializers import ZabouserSerializer, ZabouserListSerializer, ZabouserCreateSerializer
from apps.users.models import ZaboUser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from apps.notifications.helpers import SomeoneFollowingNotificatinoHelper
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from api.common.viewset import ActionAPIViewSet
from zabo.common.permissions import ZaboUserPermission

# Create your views here.
class UserViewSet(viewsets.ModelViewSet, ActionAPIViewSet):
    """
        This viewset automatically provides `list`, `create`, `retrieve`,
        `update` and `destroy` actions.

    """
    serializer_class = ZabouserSerializer
    queryset = ZaboUser.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ('nickName',)
    search_fields = ('nickName', 'email')
    # 나중에 검색 결과 순서에 대해 이야기 해보아야 함
    ordering_fields = ('nickName', 'email', 'joined_date')
    permission_classes = (ZaboUserPermission, )
    action_serializer_class = {
        'create': ZabouserCreateSerializer,
    }


    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = ZabouserListSerializer(page, many=True, context={
            'request': request,
        })
        zabouser = ZaboUser.objects.filter(email=request.user).get()
        for user in serializer.data:
            user.update({'is_following': False})
        if not (request.user.is_anonymous or zabouser.following.count() == 0):
            for user in serializer.data:
                for following in zabouser.following.all():
                    if following.email == user['email']:
                        user.update({'is_following': True})
                        break
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
        user.follow_other(nickname)
        following = get_object_or_404(ZaboUser, nickName=nickname)
        SomeoneFollowingNotificatinoHelper(notifier=user, following=following).notify_to_User()
        return Response({'Message': 'You have successfully follow'}, status=status.HTTP_201_CREATED)

    @action(methods=['post', 'delete'], detail=False)
    def unfollowOther(self, request):
        user = request.user
        nickname = request.data["nickname"]
        user.unfollow_others(nickname)
        return Response({'Message': 'You have successfully unfollow'}, status=status.HTTP_201_CREATED)
