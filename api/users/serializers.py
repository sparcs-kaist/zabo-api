from django.apps import apps as django_apps
from django.conf import base_settings
from rest_framework import serializers

from apps.users.models import User

User = django_apps.get_model(
    settings.AUTH_USER_MODEL, require_ready=False)
