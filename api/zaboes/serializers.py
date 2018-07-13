from django.apps import apps as django_apps
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api.users.serializers import ZabouserListSerializer
from apps.zaboes.models import Zabo, Timeslot, Comment, Recomment, Participate, Poster, Like
from django.conf import settings

import json


class PosterSerializer(serializers.ModelSerializer):
    image_thumbnail = serializers.ImageField(read_only=True)

    class Meta:
        model = Poster
        fields = (
            'zabo',
            'image',
            'image_thumbnail',
        )


class TimeslotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timeslot
        fields = (
            'content',
            'start_time',
            'end_time'
        )


class TimeSlotCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poster
        fields = (
            'zabo',
            'content',
            'start_time',
            'end_time'
        )


class RecommentSerializer(serializers.ModelSerializer):
    author = ZabouserListSerializer(read_only=True)

    class Meta:
        model = Recomment
        fields = '__all__'
        read_only_fields = (
            'created_time',
            'updated_time',
        )


class CommentSerializer(serializers.ModelSerializer):
    author = ZabouserListSerializer(read_only=True)
    recomments = RecommentSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = (
            'id',
            'author',
            'content',
            'created_time',
            'updated_time',
            'is_private',
            'is_deleted',
            'is_blocked',
            'recomments'
        )
        read_only_fields = (
            'created_time',
            'updated_time',
        )


class ZaboSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    posters = PosterSerializer(many=True, read_only=True)
    timeslots = TimeslotSerializer(many=True, read_only=True)

    # like_count =serializers.SerializerMethodField()

    class Meta:
        model = Zabo
        fields = (
            'founder',
            'title',
            'location',
            'content',
            'category',
            'apply',
            'payment',
            'created_time',
            'updated_time',
            'limit',
            'posters',
            'comments',
            'timeslots',
            'like_count',
            'deadline',
            'is_finished',
        )
        read_only_fields = (
            'created_time',
            'updated_time',
        )
        # auto_now_add나 auto_now가 true이면 read_only_fields여야 함.


class ZaboListSerializer(serializers.ModelSerializer):
    posters = PosterSerializer(many=True, read_only=True)
    founder = ZabouserListSerializer(read_only=True)

    class Meta:
        model = Zabo
        fields = (
            'id',
            'founder',
            'posters',
            'created_time',
            'updated_time',
            'like_count',
            # 쉽게 search, filter 결과 확인하려고 추가해 놓은 field
            'title',
            'content',
            'location',
            'deadline',
            'time_left',
            'is_finished',
        )
        read_only_fields = (
            'created_time',
            'updated_time',
        )
        # auto_now_add나 auto_now가 true이면 read_only_fields여야 함


class ZaboCreateSerializer(serializers.ModelSerializer):
    timeslots = TimeslotSerializer(many=True)

    class Meta:
        model = Zabo
        fields = (
            'title',
            'location',
            'content',
            'category',
            'apply',
            'payment',
            'timeslots',
            'deadline',
            'limit',
            # 'posters',
            # 'like_count'
        )

    def to_internal_value(self, data):
        instance = super(ZaboCreateSerializer, self).to_internal_value(data)
        if "timeslots" in data:
            # instance["id"] = 10  # That's sketchy though
            timeslot_str_data = data["timeslots"]
            timeslot_json = json.loads(timeslot_str_data)
            instance["timeslots"] = timeslot_json
        return instance

    def create(self, validated_data):

        timeslots_data = validated_data.pop('timeslots', None)
        zabo = Zabo.objects.create(**validated_data)
        if timeslots_data:
            for timeslot_data in timeslots_data:
                Timeslot.objects.create(zabo=zabo, **timeslot_data)
        return zabo;

        for poster_data in posters_data:
            Poster.objects.create(zabo=zabo, **poster_data)

        return zabo;


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('zabo', 'user')
            )
        ]
