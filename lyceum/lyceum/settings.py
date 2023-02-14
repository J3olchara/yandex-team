"""Django settings for lyceum project."""
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from dotenv import load_dotenv

if not load_dotenv(Path(r'..\.env')):
    if not load_dotenv(Path(r'.env')):
        if not load_dotenv(Path(r'example.env')):
            load_dotenv(Path(r'..\example.env'))


BASE_DIR: Path = Path(__file__).resolve().parent.parent

SECRET_KEY: str = os.getenv('SECRET_KEY', 'not_secret_key')

DEBUG: Optional[bool] = os.getenv('DJANGO_DEBUG', 'False').lower() in (
    'true',
    '1',
    't',
)

ALLOWED_HOSTS: List[str] = str(os.getenv('DJANGO_HOSTS', '*')).split()

INSTALLED_APPS: List[str] = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'about.apps.AboutConfig',
    'catalog.apps.CatalogConfig',
    'homepage.apps.HomepageConfig',
]

MIDDLEWARE: List[str] = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'lyceum.middlewares.CoffeeTime',
]

if DEBUG:
    MIDDLEWARE += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

if not os.getenv('MIDDLEWARE_REVERSE', 'False').lower() in (
    'true',
    '1',
    't',
):
    MIDDLEWARE.remove('lyceum.middlewares.CoffeeTime')

INTERNAL_IPS = [
    '127.0.0.1',
]

ROOT_URLCONF: str = 'lyceum.urls'

TEMPLATES: List[Dict[str, Any]] = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / Path(r'\homepage\templates'),
            BASE_DIR / Path(r'\about\templates'),
            BASE_DIR / Path(r'\catalog\templates'),
        ],
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

DATABASES: Dict[str, Dict[str, Union[str, Path]]] = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS: List[Dict[str, str]] = [
    {
        'NAME': 'django.contrib.auth.'
        + 'password_validation.'
        + 'UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.'
        + 'password_validation.'
        + 'MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.'
        + 'password_validation.'
        + 'CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.'
        + 'password_validation.'
        + 'NumericPasswordValidator',
    },
]

LANGUAGE_CODE: str = 'ru-ru'

TIME_ZONE: str = 'Europe/Moscow'

USE_I18N: bool = True

USE_L10N: bool = True

USE_TZ: bool = True

STATIC_URL: str = '/static/'

DEFAULT_AUTO_FIELD: str = 'django.db.models.BigAutoField'
