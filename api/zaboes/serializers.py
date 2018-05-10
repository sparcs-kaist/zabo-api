from django.apps import apps as django_apps
from rest_framework import serializers
from apps.zaboes.models import Zabo, Timeslot, Comment, Recomment, Participate
from django.conf import settings




class TimeslotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timeslot
        fields = '__all__'




class RecommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recomment
        fields = '__all__'
        read_only_fields = (
            'created_time',
            'updated_time',
        )

class CommentSerializer(serializers.ModelSerializer):
    recomments = RecommentSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = (
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
            'comments')
        read_only_fields = (
            'created_time',
            'updated_time',
        )  # auto_now_add나 auto_now가 true이면 read_only_fields여야 함.
