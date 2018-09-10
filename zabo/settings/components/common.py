import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.dirname(BASE_DIR)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'apps.users',
    'apps.zaboes',
    'apps.common',
    'apps.mails',
    'apps.notifications',
    'imagekit',
    'rest_framework_swagger',
    'corsheaders',  # django-cors-headers
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # <- 다른 것들보다 앞에 위치시켜주세요., django-cors-headers
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'zabo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'zabo.wsgi.application'


CORS_ORIGIN_ALLOW_ALL = True
INTERNAL_IPS = ('127.0.0.1', )

ALLOWD_HOSTS = ['*']

CORS_ORIGIN_ALLOW_ALL = True

base_url = ""