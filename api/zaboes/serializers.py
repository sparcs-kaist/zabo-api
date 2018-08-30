from django.apps import apps as django_apps
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api.users.serializers import ZabouserListSerializer
from apps.zaboes.models import Zabo, ZaboHistory, Timeslot, Comment, Recomment, CommentHistory, Participate, Poster, Like
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

    def create(self, validated_data):
        comment_content = validated_data.get('content', '')
        recomment = Recomment.objects.create(**validated_data)
        CommentHistory.objects.create(comment=recomment, content=comment_content)
        return recomment
    
    def update(self, instance, validated_data):
        instance.is_private = validated_data.get('is_private', instance.is_private)
        instance.is_deleted = validated_data.get('is_deleted', instance.is_deleted)
        instance.is_blocked = validated_data.get('is_blocked', instance.is_blocked)
        comment_content = validated_data.get('content', instance.content)
        if comment_content != instance.content:
            comment_history = CommentHistory.objects.create(comment=instance, content=comment_content)
        instance.content = comment_content
        instance.save()
        return instance


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
    
    def create(self, validated_data):
        comment_content = validated_data.get('content', '')
        comment = Comment.objects.create(**validated_data)
        CommentHistory.objects.create(comment=comment, content=comment_content)
        return comment
    
    def update(self, instance, validated_data):
        instance.is_private = validated_data.get('is_private', instance.is_private)
        instance.is_deleted = validated_data.get('is_deleted', instance.is_deleted)
        instance.is_blocked = validated_data.get('is_blocked', instance.is_blocked)
        comment_content = validated_data.get('content', instance.content)
        if comment_content != instance.content:
            comment_history = CommentHistory.objects.create(comment=instance, content=comment_content)
        instance.content = comment_content
        instance.save()
        return instance


class ZaboSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    posters = PosterSerializer(many=True, read_only=True)
    timeslots = TimeslotSerializer(many=True, read_only=True)
    author = ZabouserListSerializer(read_only=True)

    # like_count =serializers.SerializerMethodField()

    class Meta:
        model = Zabo
        fields = (
            'id',
            'author',
            'title',
            'location',
            'content',
            'category',
            'link_url',
            'apply',
            'payment',
            'created_time',
            'updated_time',
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

    def is_liked(self, user, zabo):
        new = self.data
        new.update({'is_liked': Like.objects.filter(user=user, zabo=zabo).exists()})
        return new


class ZaboListSerializer(serializers.ModelSerializer):
    posters = PosterSerializer(many=True, read_only=True)
    author = ZabouserListSerializer(read_only=True)

    class Meta:
        model = Zabo
        fields = (
            'id',
            'author',
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
            'link_url',
            'content',
            'category',
            'apply',
            'payment',
            'timeslots',
            'deadline',
        )

    def to_internal_value(self, data):
        instance = super(ZaboCreateSerializer, self).to_internal_value(data)
        if "timeslots" in data:
            timeslot_str_data = data["timeslots"]
            timeslot_json = json.loads(timeslot_str_data)
            instance["timeslots"] = timeslot_json
        return instance

    def create(self, validated_data):

        timeslots_data = validated_data.pop('timeslots', None)
        content_data = validated_data.get('content', '')
        zabo = Zabo.objects.create(**validated_data)
        history = ZaboHistory.objects.create(zabo=zabo, content=content_data)
        if timeslots_data:
            for timeslot_data in timeslots_data:
                Timeslot.objects.create(zabo=zabo, **timeslot_data)
        return zabo

    def update(self, instance, validated_data):

        timeslots_data = validated_data.pop('timeslots', None)
        instance.title = validated_data.get('title', instance.title)
        instance.location = validated_data.get('location', instance.location)
        instance.category = validated_data.get('category', instance.category)
        instance.apply = validated_data.get('apply', instance.apply)
        instance.payment = validated_data.get('payment', instance.payment)
        instance.deadline = validated_data.get('deadline', instance.deadline)

        new_content = validated_data.get('content', instance.content)
        if new_content != instance.content:
            ZaboHistory.objects.create(zabo=instance, content=new_content)
        instance.content = new_content

        instance.save()

        existing_time_slots = Timeslot.objects.filter(zabo=instance)
        if existing_time_slots.exists():
            for existing in  existing_time_slots.iterator():
                existing.delete()

        if timeslots_data:
            for timeslot_data in timeslots_data:
                Timeslot.objects.create(zabo=instance, **timeslot_data)
        return instance


class ZaboUrlSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Zabo
        fields = ('url',)


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
