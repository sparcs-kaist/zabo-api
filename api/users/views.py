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
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import permission_classes
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
    user = request.user
    if user.is_authenticated:
        return redirect(request.GET.get('next', '/'))

    request.session['next'] = request.GET.get('next', '/')

    login_url, state = sso_client.get_login_params()
    request.session['sso_state'] = state
    return HttpResponseRedirect(login_url)


@require_http_methods(['GET'])
def login_callback(request):
    print(3)
    next = request.session.pop('next', '/')
    state_before = request.session.get('sso_state', 'default before state')
    state = request.GET.get('state', 'default state')

    if state_before != state:
        return render(request, 'session/login_error.html',
                      {'error_title': "Login Error",
                       'error_message': "Invalid login"})

    code = request.GET.get('code')
    sso_profile = sso_client.get_user_info(code)
    username = sso_profile['sid']

    #user_list = User.objects.filter(username=username)
    try:
        kaist_info = json.loads(sso_profile['kaist_info'])
        student_id = kaist_info.get('ku_std_no')
    except:
        student_id = ''

    if student_id is None:
        student_id = ''

    # if len(user_list) == 0:
    #     user = User.objects.create_user(username=username,
    #                                     email=sso_profile['email'],
    #                                     password=str(random.getrandbits(32)),
    #                                     first_name=sso_profile['first_name'],
    #                                     last_name=sso_profile['last_name'])
    #     user.save()
    #
    #     try:
    #         user_profile = UserProfile.objects.get(student_id=sso_profile['sid'])
    #         user_profile.user = user
    #     except:
    #         user_profile = UserProfile(student_id=student_id, user=user)
    #
    #     user_profile.sid = sso_profile['sid']
    #     user_profile.save()
    #
    #     if not settings.DEBUG:
    #         os.chdir('/var/www/otlplus/')
    #     os.system('python do_import_user_major.py %s' % student_id)
    #     os.system('python update_taken_lecture_user.py %s' % student_id)
    #     OldTimeTable.import_in_for_user(student_id)
    #
    #     user = authenticate(username=username)
    #     login(request, user)
    #     return redirect(next)
    # else:
    #     user = authenticate(username=user_list[0].username)
    #     user.first_name = sso_profile['first_name']
    #     user.last_name = sso_profile['last_name']
    #     user.save()
    #     user_profile = UserProfile.objects.get(user=user)
    #     previous_student_id = user_profile.student_id
    #     user_profile.student_id = student_id
    #     user_profile.save()
    #     if previous_student_id != student_id:
    #         if not settings.DEBUG:
    #             os.chdir('/var/www/otlplus/')
    #         os.system('python do_import_user_major.py %s' % student_id)
    #         os.system('python update_taken_lecture_user.py %s' % student_id)
    #         OldTimeTable.import_in_for_user(student_id)
    #     login(request, user)
    #     return redirect(next)
    # return render(request, 'session/login_error.html',
    #               {'error_title': "Login Error",
    #                'error_message': "No such that user"})

@permission_classes((IsAuthenticated, ))
def logout(request):
    return

@permission_classes((IsAuthenticated, ))
def unregister(request):
    return