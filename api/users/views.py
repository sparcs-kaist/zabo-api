from rest_framework import viewsets
from api.users.serializers import ZabouserSerializer, ZabouserListSerializer, ZabouserCreateSerializer
from apps.users.models import ZaboUser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework import status
from apps.notifications.helpers import SomeoneFollowingNotificatinoHelper
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from apps.users.sparcssso import Client
from zabo.settings.components.secret import SSO_CLIENT_ID, SSO_SECRET_KEY, SSO_IS_BETA
from rest_framework.generics import RetrieveAPIView
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import permission_classes
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_auth
from django.views.decorators.csrf import csrf_exempt
from api.common.viewset import ActionAPIViewSet
from zabo.common.permissions import ZaboUserPermission
import json
import random
import os
from operator import eq
from zabo.settings.components.common import base_url
from rest_framework_jwt.settings import api_settings

sso_client = Client(SSO_CLIENT_ID, SSO_SECRET_KEY, SSO_IS_BETA)

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
    # 나중에 검색 결과s 순서에 대해 이야기 해보아야 함
    ordering_fields = ('nickName', 'email', 'joined_date')
    permission_classes = (ZaboUserPermission, )
    action_serializer_class = {
        'create': ZabouserCreateSerializer,
    }


    def list(self, request):
        print("Zabouser list")
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = ZabouserListSerializer(page, many=True, context={
            'request': request,
        })
        for user in serializer.data:
            user.update({'is_following': False})
        #if not request.user.is_anonymous:	
        #    zabouser = ZaboUser.objects.filter(email=request.user).get() 
        if not request.user.is_anonymous:
            zabouser = ZaboUser.objects.filter(email=request.user).get()
            if not zabouser.following.count() == 0:
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
        user.unfollow_other(nickname)
        return Response({'Message': 'You have successfully unfollow'}, status=status.HTTP_201_CREATED)

# front end base url
# url after login
url_after_login = base_url + "/login/"
# url when get error
url_when_error = base_url + "/error/"
# url after logout
url_after_logout = base_url


def login(request):
    user = request.user
    if user.is_authenticated:
        return redirect(url_after_login)

    login_url, state = sso_client.get_login_params()
    request.session['sso_state'] = state
    return redirect(login_url)


@require_http_methods(['GET'])
def login_callback(request):
    state_before = request.session.get('sso_state', 'default before state')
    state = request.GET.get('state', 'default state')
    if state_before != state:
        return redirect(url_when_error)

    code = request.GET.get('code')
    sso_profile = sso_client.get_user_info(code)
    #print(sso_profile)
    email = sso_profile['email']
    user_list = ZaboUser.objects.filter(email=email)

    if len(user_list) == 0:
        user = ZaboUser.objects.create_user(email=email, password=email)

        sso_gender = sso_profile['gender']
        if eq(sso_gender, "M"):
            user.gender = "M"
        elif eq(sso_gender, "F"):
            user.gender = "F"
        elif eq(sso_gender, "H"):
            user.gender = "B"
        elif eq(sso_gender, "E"):
            user.gender = "E"
        user.sid = sso_profile['sid']
        #TODO sso유저 닉네임 설정
        user.nickName = email.split('@')[0]
        if sso_profile["first_name"]:
            user.first_name = sso_profile["first_name"]
        else:
            user.first_name = "blank"
        if sso_profile["last_name"]:
            user.last_name = sso_profile["last_name"]
        else:
            user.last_name = "blank"
        print("user's sid: {sid}".format(sid=user.sid))
        user.is_sso = True
        user.save()

    else:
        print("user exists")
        user = user_list[0]
        user.nickName = email.split('@')[0]
        user.first_name = sso_profile['first_name']
        user.last_name = sso_profile['last_name']
        sso_gender = sso_profile['gender']
        if eq(sso_gender, "M"):
            user.gender = "M"
        elif eq(sso_gender, "F"):
            user.gender = "F"
        elif eq(sso_gender, "H"):
            user.gender = "B"
        elif eq(sso_gender, "E"):
            user.gender = "E"
        user.sid = sso_profile['sid']
        user.is_sso = True
        user.save()

    next_path = '{0}{1}'.format(url_after_login, api_settings.JWT_ENCODE_HANDLER(
        api_settings.JWT_PAYLOAD_HANDLER(
            user,
        )
    ))

    return redirect(next_path)

    return JsonResponse(status=200,
                        data={'error_title': "Login Error",
                              'error_message': "No such that user"})


@api_view(['GET'])
def logout(request):
    print("logout")
    email = request.GET.get('email')
    sid = ZaboUser.objects.get(email=email).sid
    logout_url = sso_client.get_logout_url(sid, url_after_logout)
    return redirect(logout_url)

    if request.user.is_authenticated:
        sid = ZaboUser.objects.get(email=request.GET.get('email')).sid
        logout_url = sso_client.get_logout_url(sid, url_after_logout)
        request.session['visited'] = True
        return redirect(logout_url)
    return redirect(url_after_logout)


@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated,])
def unregister(request):
    if request.method != 'POST':
        return JsonResponse(status=200,
                            data={'error_title': "Unregister Error",
                                  'error_message': "please try again1"})
    zabo_user = ZaboUser.objects.get(email=request.user)

    sid = zabo_user.sid
    result = sso_client.do_unregister(sid)
    if not result:
        return JsonResponse(status=200,
                            data={'error_title': "Unregister Error",
                                  'error_message': "please try again2"})

    zabo_user.delete()
    user.delete()

    return JsonResponse(status=200,
                        data={'message': "Unregister successfully"})
