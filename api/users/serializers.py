from django.apps import apps as django_apps
from rest_framework import serializers

from apps.users.models import ZaboUser


class ZabouserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZaboUser
        fields = (
            'email',
        )
        #fields = '__all__'
        read_only_fields = (
            'joined_date',
        )  # auto_now_add나 auto_now가 true이면 read_only_fields여야 함.

class ZabouserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZaboUser
        fields = (
            'email',
            'nickName',
            'first_name',
            'last_name',
            'joined_date',
        )
        read_only_fields = (
            'joined_date',
        )