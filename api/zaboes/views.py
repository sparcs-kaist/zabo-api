from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets, mixins

from apps.zaboes.models import Zabo,Poster
from api.zaboes.serializers import ZaboSerializer, PosterSerializer, ZaboCreateSerializer
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from zabo.common.permissions import IsOwnerOrReadOnly
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from api.common.viewset import ActionAPIViewSet
from rest_framework.permissions import IsAuthenticated


# Create your views here.

class ZaboViewSet(viewsets.ModelViewSet, ActionAPIViewSet):
    """
        This viewset automatically provides `list`, `create`, `retrieve`,
        `update` and `destroy` actions.

    """
    serializer_class = ZaboSerializer
    queryset = Zabo.objects.all()
    action_serializer_class = {
        'create': ZaboCreateSerializer,
    }

    def list(self, request):
        serializer = ZaboSerializer(self.queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        zabo = serializer.save(
            founder=self.request.user
        )

        # save poster instance (can be more than one)
        for i in range(len(request.FILES)):
            # 현재는 posters array에서 각각(posters[0], posters[1])이렇게 접근하는 방법을
            # 몰라서 이렇게 해놓음, 확인 바람
            poster = request.FILES['posters['+str(i)+']']
            instance = Poster(zabo=zabo, image=poster)
            instance.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    def perform_create(self, serializer):
        serializer.save(
            founder=self.request.user
        )

    def retrieve(self, request, pk=None):
        zabo = get_object_or_404(self.queryset, pk=pk)
        serializer = ZaboSerializer(zabo, context={'request': request})

        return Response(serializer.data)

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass


class PosterViewSet(viewsets.ModelViewSet):
    serializer_class = PosterSerializer
    queryset = Poster.objects.all()

    def perform_create(self, serializer):
        serializer.save()

