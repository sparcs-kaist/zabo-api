from rest_framework import viewsets
from api.notifications import serializers
from apps.notifications.models import ZaboReactionNotification
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from apps.notifications.helpers import get_sorted_noti_list_by_user, convert_noti_list_to_queryset


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
        noti_list = get_sorted_noti_list_by_user(user)
        noti_queryset = convert_noti_list_to_queryset(request, noti_list)
        page = self.paginate_queryset(noti_queryset)

        if page is not None:
            return self.get_paginated_response(page)
        return Response("No page")

