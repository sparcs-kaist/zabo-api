from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from apps.zaboes.models import Zabo
from apps.zaboes.serializers import ZaboSerializer
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from zabo.common.permissions import IsOwnerOrReadOnly
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


# Create your views here.

class ZaboViewSet(viewsets.ModelViewSet):
    """
        This viewset automatically provides `list`, `create`, `retrieve`,
        `update` and `destroy` actions.

    """
    serializer_class = ZaboSerializer
    queryset = Zabo.objects.all()

    def list(self, request):
        serializer = ZaboSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(
            founder=self.request.user
        )

    def retrieve(self, request, pk=None):
        zabo = get_object_or_404(self.queryset, pk=pk)
        serializer = ZaboSerializer(zabo)
        return Response(serializer.data)

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass
