from django.apps import apps as django_apps
from rest_framework import serializers

from apps.users.models import ZaboUser

class ZabouserFollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZaboUser
        fields = (
            'id',
            'profile_image',
        )

class ZabouserSerializer(serializers.ModelSerializer):
    following = ZabouserFollowingSerializer(many=True, read_only=True)

    class Meta:
        model = ZaboUser
        exclude = ('is_staff', 'phone', 'password')
        read_only_fields = (
            'joined_date',
        )  # auto_now_add나 auto_now가 true이면 read_only_fields여야 함.


class ZabouserListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ZaboUser
        fields = (
            'id',
            'email',
            'url',
            'nickName',
            'profile_image',
        )