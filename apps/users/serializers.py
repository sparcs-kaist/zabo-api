from django.apps import apps as django_apps
from rest_framework import serializers

from apps.users.models import ZaboUser


class ZabouserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZaboUser
        fields = '__all__'
        read_only_fields = (
            'joined_date'
        )  # auto_now_add나 auto_now가 true이면 read_only_fields여야 함.
