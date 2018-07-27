from rest_framework import viewsets
from api.users.serializers import ZabouserSerializer, ZabouserListSerializer
from apps.users.models import ZaboUser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
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
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as login_auth
import json
import random
import os

sso_client = Client(SSO_CLIENT_ID, SSO_SECRET_KEY, SSO_IS_BETA)


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
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
    permission_classes = ('')

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


def login(request):
    # print("login")
    user = request.user
    # print("user is {user}".format(user=user))
    if user.is_authenticated:
        return redirect(request.GET.get('next', '/'))

    request.session['next'] = request.GET.get('next', '/')

    login_url, state = sso_client.get_login_params()
    request.session['sso_state'] = state
    # print("state is {state}".format(state=state))
    return HttpResponseRedirect(login_url)


@require_http_methods(['GET'])
def login_callback(request):
    # print("login_callback")
    next = request.session.pop('next', '/')
    state_before = request.session.get('sso_state', 'default before state')
    state = request.GET.get('state', 'default state')

    if state_before != state:
        return JsonResponse(status=200,
                            data={'error_title': "Login Error",
                       'error_message': "Invalid login"})
        # return render(request, 'session/login_error.html',
        #               {'error_title': "Login Error",
        #                'error_message': "Invalid login"})

    code = request.GET.get('code')
    sso_profile = sso_client.get_user_info(code)

    email = sso_profile['email']

    user_list = ZaboUser.objects.filter(email=email)

    if len(user_list) == 0:
        user = ZaboUser.objects.create_user(email=email, password=email)
        user.first_name = sso_profile['first_name']
        user.last_name = sso_profile['last_name']
        user.gender = sso_profile['gender']
        user.sid = sso_profile['sid']
        user.save()

        # user = authenticate(email=email)
        login_auth(request, user)
        return JsonResponse(status=200,
                            data={'message': "Login success, new zabo user"})
        #return redirect(next)
    else:
        user = user_list[0]
        user.first_name = sso_profile['first_name']
        user.last_name = sso_profile['last_name']
        user.save()
        login_auth(request, user)
        return JsonResponse(status=200,
                            data={'message': "Login success, existed zabo user"})
        #return redirect(next)

    return JsonResponse(status=200,
                        data={'error_title': "Login Error",
                              'error_message': "No such that user"})
    # return render(request, 'session/login_error.html',
    #               {'error_title': "Login Error",
    #                'error_message': "No such that user"})


@permission_classes((IsAuthenticated,))
def logout(request):
    if request.user.is_authenticated:
        sid = ZaboUser.objects.get(email=request.email).sid
        redirect_url = request.GET.get('next', request.build_absolute_uri('/'))
        logout_url = sso_client.get_logout_url(sid, redirect_url)
        logout(request)
        request.session['visited'] = True
        return redirect(logout_url)
    return redirect("/main")


@permission_classes((IsAuthenticated,))
def unregister(request):
    if request.method != 'POST':
        return JsonResponse(status=200,
                            data={'error_title': "Unregister Error",
                                  'error_message': "please try again"})
        # return render(request, 'session/login_error.html',
        #               {'error_title': "Unregister Error",
        #                'error_message': "please try again"})

    user = request.user
    zabo_user = ZaboUser.objects.get(user=user)

    sid = zabo_user.sid
    result = sso_client.do_unregister(sid)
    if not result:
        return JsonResponse(status=200,
                            data={'error_title': "Unregister Error",
                                  'error_message': "please try again"})
        # return render(request, 'session/login_error.html',
        #               {'error_title': "Unregister Error",
        #                'error_message': "please try again"})

    zabo_user.delete()
    user.delete()
    logout(request)

    return JsonResponse(status=200, data={})
