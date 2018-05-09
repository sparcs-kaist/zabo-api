from django.apps import apps as django_apps
from rest_framework import serializers
from apps.zaboes.models import Zabo, Timeslot, Comment, Recomment, Participate, Poster
from django.conf import settings


class ZaboSerializer(serializers.ModelSerializer):
    posters = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='poster-detail'
    )

    class Meta:
        model = Zabo
        fields = (
            'founder',
            'location',
            'content',
            'category',
            'apply',
            'payment',
            'created_time',
            'updated_time',
            'limit',
            'posters'
        )
        read_only_fields = (
            'created_time',
            'updated_time',
        )  # auto_now_add나 auto_now가 true이면 read_only_fields여야 함.


class PosterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poster
        fields = (
            'zabo',
            'image',
        )


class ZaboCreateSerializer(serializers.ModelSerializer):
    posters = PosterSerializer(many=True, read_only=True)

    class Meta:
        model = Zabo
        fields = (
            'location',
            'content',
            'category',
            'apply',
            'payment',
            'limit',
            #'deadline',
            'posters',
        )


class TimeslotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timeslot
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = (
            'created_time',
            'updated_time',
        )


class RecommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recomment
        fields = '__all__'
        read_only_fields = (
            'created_time',
            'updated_time',
        )



