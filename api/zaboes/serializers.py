from django.apps import apps as django_apps
from django.conf import base_settings
from rest_framework import serializers

from apps.zaboes.models import Zabo

Zabo = django_apps.get_model(
    settings.ZABO_MODEL, require_ready=True)
