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
        email = request.data["email"]
        target_user = get_object_or_404(self.queryset, email=email)
        if target_user.is_sso:
            return Response("This API does not work for sso members")
        target_user.is_active = True
        target_user.save()
        return Response("Sucessfully verified")

    @action(methods=["patch"], detail=False)
    def change_password(self, request):
        email = request.data["email"]
        new_password = request.data["password"]
        target_user = get_object_or_404(self.queryset, email=email)
        if target_user.is_sso:
            return Response("This API does not work for sso members")
        target_user.set_password(new_password)
        target_user.save()
        return Response("Sucessfully chaged")




