from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from apps.zaboes.models import *
from api.zaboes.serializers import ZaboSerializer, CommentSerializer, RecommentSerializer
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from zabo.common.permissions import IsOwnerOrReadOnly
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import status
# Create your views here.
from zabo.common.permissions import IsAuthenticated


class ZaboViewSet(viewsets.ModelViewSet):
    """
        This viewset automatically provides `list`, `create`, `retrieve`,
        `update` and `destroy` actions.

    """
    serializer_class = ZaboSerializer
    queryset = Zabo.objects.all()
    # permission_classes = (IsAuthenticated, )


    def list(self, request):
        serializer = ZaboSerializer(self.queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(
            founder=self.request.user
        )

    def retrieve(self, request, pk=None):
        zabo = get_object_or_404(self.queryset, pk=pk)
        if(zabo.is_deleted):
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = ZaboSerializer(zabo, context={'request': request})
        return Response(serializer.data)


    def destroy(self, request, pk=None):
        instance = get_object_or_404(self.queryset, pk=pk)
        setattr(instance, "is_deleted", True)
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def list(self, request):
        serializer = CommentSerializer(self.queryset, many=True, context={'request': request})
        return Response(serializer.data)


    def perform_create(self, serializer):
        zabo_id = int(self.request.data["zabo"])
        zabo = get_object_or_404(Zabo.objects.all(), pk=zabo_id)

        serializer.save(
            author=self.request.user,
            zabo=zabo
        )



class RecommentViewSet(viewsets.ModelViewSet):
    serializer_class = RecommentSerializer
    queryset = Recomment.objects.all()

    def list(self, request):
        serializer = self.get_serializer(self.queryset, many=True, context={'request': request})
        return Response(serializer.data)


    def perform_create(self, serializer):
        comment_id = int(self.request.data["comment"])
        comment = get_object_or_404(Comment.objects.all(), pk=comment_id)

        serializer.save(
            comment = comment,
            author=self.request.user,
        )



