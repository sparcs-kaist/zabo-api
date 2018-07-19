import os

from django.conf import settings

STATIC_URL = '/static/'
STATICFILES_DIRS = ()
STATIC_ROOT = os.path.join(settings.ROOT_DIR, 'assets')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(settings.ROOT_DIR, 'media')
