from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import viewsets
from apps.mails.models import ZaboMail
from apps.mails.helpers import MailHelpers
from api.mails.serializers import PaperMailCreateSerializer
from api.common.viewset import ActionAPIViewSet
from zabo.common.permissions import ZaboMailPermission
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from zabo.settings.components.mail import ADMIN_MAIL

class ZaboMailViewSet(viewsets.ModelViewSet, ActionAPIViewSet):
    """
        This viewset automatically provides `list`, `create`, `retrieve`,
        `update` and `destroy` actions.
    """
    serializer_class = PaperMailCreateSerializer
    queryset = ZaboMail.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    search_fields = ('sender_address', 'message',)
    # 나중에 검색 결과 순서에 대해 이야기 해보아야 함
    ordering_fields = ('created_time',)
    permission_classes = (ZaboMailPermission,)

    def perform_create(self, serializer):
        paperMail = serializer.save()
        MailHelpers(paperMail).sendMail()

    @action(methods=['POST'],detail=False)
    def report(self, request):
        if request.user.is_anonymous:
            return Response({'Message': 'You are unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reportMail = serializer.save(sender_address = user.email, receivers_address = ADMIN_MAIL )
        MailHelpers(reportMail).sendMail()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
