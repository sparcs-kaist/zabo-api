from rest_framework import serializers
from apps.mails.models import ZaboMail
import json


class PaperMailCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZaboMail
        fields = '__all__'

    def to_internal_value(self, data):
        instance = super(PaperMailCreateSerializer, self).to_internal_value(data)
        if "receivers_address" in data:
            receivers_data = data["receivers_address"]
            receivers_list = receivers_data.split(",")
            instance["receivers_address"] = ':'.join(receivers_list)
        return instance
