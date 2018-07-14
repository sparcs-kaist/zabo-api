from rest_framework import serializers

from apps.notifications.models import ZaboReactionNotification, BaseNotification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZaboReactionNotification
        fields = '__all__'
        read_only_fields = (
            'created_time',
            'updated_time',
        )