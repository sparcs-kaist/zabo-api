from rest_framework.views import APIView
from rest_framework.response import Response
from zabo.common.permissions import AdminUserPermission
from rest_framework.decorators import action
from rest_framework import viewsets
from apps.users.models import ZaboUser
from django.shortcuts import get_object_or_404


class AdminViewSet(viewsets.ModelViewSet):
    queryset = ZaboUser.objects.all()
    permission_classes = (AdminUserPermission,)

    @action(methods=["patch"], detail=False)
    def validate_user(self, request):
        nickName = request.data["nickName"]
        target_user = get_object_or_404(self.queryset, nickName=nickName)
        target_user.is_active = True
        target_user.save()
        return Response("Sucessfully verified")

    @action(methods=["patch"], detail=False)
    def change_password(self, reqeust):
        return Response("It worked 2")




