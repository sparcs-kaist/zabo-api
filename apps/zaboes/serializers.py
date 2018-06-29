from django.apps import apps as django_apps
from rest_framework import serializers
from apps.zaboes.models import Zabo, Timeslot, Comment, Recomment, Participate
from django.conf import settings

"""
class ZaboSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zabo
        fields = '__all__'
        read_only_fields = (
            'created_time',
            'updated_time',
        )  # auto_now_add나 auto_now가 true이면 read_only_fields여야 함.
"""

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
        model = Comment
        fields = '__all__'
        read_only_fields = (
            'created_time',
            'updated_time',
        )
