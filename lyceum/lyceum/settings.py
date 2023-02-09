import os
from pathlib import Path

from typing import Union, Optional


BASE_DIR: Path = Path(__file__).resolve().parent.parent

SECRET_KEY: Union[None, str] = os.getenv('SECRET_KEY')

DEBUG: bool = True

ALLOWED_HOSTS: list[str] = []

INSTALLED_APPS: list[str] = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'about.apps.AboutConfig',
    'catalog.apps.CatalogConfig',
    'homepage.apps.HomepageConfig',
]

MIDDLEWARE: list[str] = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF: str = 'lyceum.urls'

TEMPLATES: list[dict[str, Union[str, list, bool, dict[str, list[str]]]]] = [
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

WSGI_APPLICATION: str = 'lyceum.wsgi.application'

DATABASES: dict[str, dict[str, str | Path]] = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS: list[dict[str, str]] = [
    {
        'NAME': 'django.contrib.auth.' +
                'password_validation.' +
                'UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.' +
                'password_validation.' +
                'MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.' +
                'password_validation.' +
                'CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.' +
                'password_validation.' +
                'NumericPasswordValidator',
    },
]

LANGUAGE_CODE: str = 'ru-ru'

TIME_ZONE: str = 'Europe/Moscow'

USE_I18N: bool = True

USE_L10N: bool = True

USE_TZ: bool = True

STATIC_URL: str = '/static/'

DEFAULT_AUTO_FIELD: str = 'django.db.models.BigAutoField'
