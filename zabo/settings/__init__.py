from os import environ

from split_settings.tools import include, optional

ENV = environ.get('ZABO_ENV') or 'development'

base_settings = [
    'components/common.py',
    optional('components/secret.py'),
    optional('components/database.py'),
    'components/locale.py',
    'components/model.py',
    'components/rest_framework.py',
    'components/static.py',
    'environments/%s.py' % ENV,
]

include(*base_settings)
