from rest_framework import viewsets
from api.notifications import serializers
from apps.notifications.models import ZaboReactionNotification, CommentReactionNotification, ZaboFollowingNotification, \
    SomeoneFollowingNotification
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from apps.notifications.helpers import SomeoneFollowingNotificatinoHelper
from django.shortcuts import get_object_or_404
from itertools import chain
from collections import OrderedDict
from api.zaboes.serializers import ZaboUrlSerializer


# Create your views here.
class NotificationViewSet(viewsets.ModelViewSet):
    """
        This viewset automatically provides `list`, `create`, `retrieve`,
        update` and `destroy` actions.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.NotificationSerializer
    queryset = ZaboReactionNotification.objects.all()

    def list(self, request):

        user = request.user
        noti_list = self.get_sorted_noti_list_by_user(user)
        noti_queryset = self.convert_noti_list_to_queryset(noti_list)
        page = self.paginate_queryset(noti_queryset)

        if page is not None:
            return self.get_paginated_response(page)
        return Response("No page")

    # get querysets from various noti models & combine them  & sort them by updated time
    def get_sorted_noti_list_by_user(self, user):
        ZaboReactors = ZaboReactionNotification.objects.filter(to=user)
        CommentReactors = CommentReactionNotification.objects.filter(to=user)
        ZaboFollowings = ZaboFollowingNotification.objects.filter(to=user)
        SomeoneFollowings = SomeoneFollowingNotification.objects.filter(to=user)
        result_list = sorted(
            chain(ZaboReactors, CommentReactors, ZaboFollowings, SomeoneFollowings),
            key=lambda instance: instance.updated_time, reverse=True)
        return result_list

    def convert_noti_list_to_queryset(self, noti_list):
        ret = []
        context = {"request": self.request}
        try:
            for noti in noti_list:
                ret_noti = {}
                if isinstance(noti, ZaboReactionNotification):
                    serializer = ZaboUrlSerializer(noti.zabo, context=context)
                    ret_noti["reactors_count"] = noti.reactors_count
                    ret_noti["content"] = noti.content
                    ret_noti["from"] = noti.reactors.first().nickName
                    ret_noti["url"] = serializer.data["url"]
                    ret_noti["type"] = "ZaboReaction"
                elif isinstance(noti, CommentReactionNotification):
                    serializer = ZaboUrlSerializer(noti.comment.zabo, context=context)
                    ret_noti["reactors_count"] = noti.reactors_count
                    ret_noti["content"] = noti.content
                    ret_noti["from"] = noti.reactors.first().nickName
                    ret_noti["url"] = serializer.data["url"]
                    ret_noti["type"] = "CommentReaction"
                elif isinstance(noti, ZaboFollowingNotification):
                    serializer = ZaboUrlSerializer(noti.zabo, context=context)
                    ret_noti["from"] = noti.following.nickName
                    ret_noti["content"] = noti.content
                    ret_noti["url"] = serializer.data["url"]
                    ret_noti["type"] = "ZaboFollowing"
                elif isinstance(noti, SomeoneFollowingNotification):
                    ret_noti["from"] = noti.following.nickName
                    ret_noti["type"] = "SomeoneFollowing"
                else:
                    print(noti, 'unexpected type notification')
                    raise StopIteration
                ret_noti["updated_at"] = noti.updated_time
                ret.append(ret_noti)
            return ret
        except StopIteration:
            print("well stopped")
