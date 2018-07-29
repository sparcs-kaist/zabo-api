import os
from subprocess import call
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "zabo.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
#call('python manage.py runserver 127.0.0.1:8000')
