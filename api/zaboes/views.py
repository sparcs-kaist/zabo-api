from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework import viewsets
from apps.zaboes.models import *
from api.zaboes.serializers import *
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from zabo.common.permissions import IsOwnerOrReadOnly
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from api.common.viewset import ActionAPIViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action


# Create your views here.

class ZaboViewSet(viewsets.ModelViewSet, ActionAPIViewSet):
    """
        This viewset automatically provides `list`, `create`, `retrieve`,
        `update` and `destroy` actions.
    """
    serializer_class = ZaboSerializer
    queryset = Zabo.objects.all()
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filter_fields = ('category', 'apply', 'payment')
    search_fields = ('title', 'content', 'location')
    # 나중에 검색 결과 순서에 대해 이야기 해보아야 함
    ordering_fields = ('title', 'likes', 'created_time')

    action_serializer_class = {
        'create': ZaboCreateSerializer,
        'list': ZaboListSerializer,
        'retrieve': ZaboSerializer,
        "update": ZaboUpdateSerializer
    }

    permission_classes = (AllowAny,)

    # permission_classes = (IsAuthenticated, )

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)

        if page is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'Message': 'You have successfully register'}, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):

        zabo = serializer.save(
            founder=self.request.user
        )

        # save poster instance (can be more than one)

        for key, file in self.request.FILES.items():
            instance = Poster(zabo=zabo, image=file)
            instance.save()
    #
    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #
    #     if getattr(instance, '_prefetched_objects_cache', None):
    #         # If 'prefetch_related' has been applied to a queryset, we need to
    #         # forcibly invalidate the prefetch cache on the instance.
    #         instance._prefetched_objects_cache = {}
    #
    #     return Response(serializer.data)

    def perform_update(self, serializer):
        zabp = serializer.save(founder=self.request.user)



    def retrieve(self, request, pk=None):
        zabo = get_object_or_404(self.queryset, pk=pk)
        if (zabo.is_deleted):
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = self.get_serializer(zabo)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        instance = get_object_or_404(self.queryset, pk=pk)
        setattr(instance, "is_deleted", True)
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False)
    def created(self, request):
        user = request.user
        queryset = Zabo.objects.filter(founder=user).order_by('updated_time')
        page = self.paginate_queryset(queryset)
        serializer = ZaboListSerializer(page, many=True, context={
            'request': request,
        })
        if page is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def popular(self, request):
        queryset = Zabo.objects.all()
        queryset = sorted(queryset, key=lambda zabo: (-zabo.like_count))
        page = self.paginate_queryset(queryset)
        serializer = ZaboListSerializer(page, many=True, context={
            'request': request,
        })
        if page is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def soon(self, request):
        queryset = Zabo.objects.all()
        queryset = (zabo for zabo in queryset if not zabo.is_finished)
        queryset = sorted(queryset, key=lambda zabo: (zabo.time_left))
        page = self.paginate_queryset(queryset)
        serializer = ZaboListSerializer(page, many=True, context={
            'request': request,
        })
        if page is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)


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
            comment=comment,
            author=self.request.user,
        )


class PosterViewSet(viewsets.ModelViewSet):
    serializer_class = PosterSerializer
    queryset = Poster.objects.all()


class LikeViewSet(viewsets.ModelViewSet):
    serializer_class = LikeSerializer
    queryset = Like.objects.all()

    def create(self, request, *args, **kwargs):
        user = request.user
        newdata = request.data.copy()
        newdata['user'] = user.id

        serializer = self.get_serializer(data=newdata)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=['delete'], detail=False)
    def dislike(self, request):
        user_id = int(request.user.id)
        print("user_id: " + str(user_id))
        zabo_id = int(request.data["zabo"])
        print("zabo_id: " + str(zabo_id))
        instance = Like.objects.filter(user=user_id).filter(zabo=zabo_id)
        self.perform_destroy(instance)
        return Response({'Message': 'You have successfully dislike'}, status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()
