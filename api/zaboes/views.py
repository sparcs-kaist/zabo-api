from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework import viewsets
from apps.zaboes.models import *
from api.zaboes.serializers import *
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from zabo.common.permissions import IsOwnerOrIsAuthenticatdThenCreateOnlyOrReadOnly
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from api.common.viewset import ActionAPIViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from apps.notifications.helpers import ReactionNotificatinoHelper, FollowingNotificatinoHelper
from zabo.common.permissions import IsOwnerOrIsAuthenticatdThenCreateOnlyOrReadOnly
from apps.zaboes.helpers import get_random_zabo
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
        "update": ZaboCreateSerializer
    }

    permission_classes = (IsOwnerOrIsAuthenticatdThenCreateOnlyOrReadOnly, )

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)

        if page is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)

    def perform_create(self, serializer):
        zabo = serializer.save(
            author=self.request.user
        )
        # save poster instance (can be more than one)
        for key, file in self.request.FILES.items():
            instance = Poster(zabo=zabo, image=file)
            instance.save()
        # make notification to followings
        followers = zabo.author.follower.all()
        if followers.exists():
            for follower in followers.iterator():
                FollowingNotificatinoHelper(notifier=zabo.author, to=follower).notify_to_User(zabo)
            
    def perform_update(self, serializer):
        zabo = serializer.save(founder=self.request.user)
        for poster in zabo.posters.all():
            poster.delete()
        for key, file in self.request.FILES.items():
            instance = Poster(zabo=zabo, image=file)
            instance.save()

    def retrieve(self, request, pk=None):
        zabo = get_object_or_404(self.queryset, pk=pk)
        if (zabo.is_deleted):
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = self.get_serializer(zabo)
        if request.user.is_anonymous:
            new = serializer.data
            new.update({'is_liked': False})
            return Response(new)
        new = serializer.is_liked(request.user, zabo)
        return Response(new)

    def destroy(self, request, pk=None):
        instance = get_object_or_404(self.queryset, pk=pk)
        setattr(instance, "is_deleted", True)
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False)
    def created(self, request):
        if request.user.is_anonymous:
            return Response({'Message': 'You are unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        user = request.user
        queryset = Zabo.objects.filter(author=user).order_by('updated_time')
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

    @action(methods=['get'], detail=False)
    def random(self, request):
        zabo = get_random_zabo()
        serializer = self.get_serializer(zabo)
        if request.user.is_anonymous:
            new = serializer.data
            new.update({'is_liked': False})
            return Response(new)
        new = serializer.is_liked(request.user, zabo)
        return Response(new)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = (IsOwnerOrIsAuthenticatdThenCreateOnlyOrReadOnly,)

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
        # Make notification to ZaboUser
        ReactionNotificatinoHelper(self.request.user).notify_to_User(zabo)


class RecommentViewSet(viewsets.ModelViewSet):
    serializer_class = RecommentSerializer
    queryset = Recomment.objects.all()
    permission_classes = (IsOwnerOrIsAuthenticatdThenCreateOnlyOrReadOnly, )

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
        # Make notification to CommentUser
        ReactionNotificatinoHelper(self.request.user).notify_to_User(comment)


class PosterViewSet(viewsets.ModelViewSet):
    serializer_class = PosterSerializer
    queryset = Poster.objects.all()
    permission_classes = (IsAdminUser,)


class LikeViewSet(viewsets.ModelViewSet):
    serializer_class = LikeSerializer
    queryset = Like.objects.all()
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        user = request.user
        newdata = request.data.copy()
        newdata['user'] = user.id
        serializer = self.get_serializer(data=newdata)
        serializer.is_valid(raise_exception=True)
        like = serializer.save()
        ReactionNotificatinoHelper(user).notify_to_User(like.zabo)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=['delete'], detail=False)
    def dislike(self, request):
        user_id = int(request.user.id)
        zabo_id = int(request.data["zabo"])
        instance = Like.objects.filter(user=user_id).filter(zabo=zabo_id)
        ReactionNotificatinoHelper(request.user).cancel_reaction(get_object_or_404(Zabo.objects.all(), pk=zabo_id))
        self.perform_destroy(instance)
        return Response({'Message': 'You have successfully dislike'}, status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        return instance.delete()
