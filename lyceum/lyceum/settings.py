"""
Django settings for lyceum project.

!!!!!!!!!!!!!DO NOT ENABLE DEBUG IN PRODUCTION!!!!!!!!!!!!!!!
"""
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from django.utils.translation import ugettext_lazy as _
from dotenv import load_dotenv

BASE_DIR: Path = Path(__file__).resolve().parent.parent

if not load_dotenv(BASE_DIR.parent / '.env'):
    load_dotenv(BASE_DIR.parent / 'example.env')

# --------------------------------------------------------------------
# ------------------------Site info Section---------------------------
# --------------------------------------------------------------------

SITE_EMAIL = os.getenv('SITE_EMAIL')

# --------------------------------------------------------------------
# ------------------------Project Parameters Section------------------
# --------------------------------------------------------------------

SECRET_KEY: str = os.getenv('SECRET_KEY', 'not_secret_key')

DEBUG: Optional[bool] = os.getenv('DJANGO_DEBUG', 'False').lower() in (
    'true',
    '1',
    't',
)

ALLOWED_HOSTS: List[str] = str(os.getenv('DJANGO_HOSTS', '*')).split()

REVERSER_MIDDLEWARE = os.getenv('MIDDLEWARE_REVERSE', 'False').lower() in (
    'true',
    '1',
    't',
)

# --------------------------------------------------------------------
# ----------------------------Apps Section----------------------------
# --------------------------------------------------------------------


INSTALLED_APPS: List[str] = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

CUSTOM_APPS = [
    'core.apps.CoreConfig',
    'about.apps.AboutConfig',
    'catalog.apps.CatalogConfig',
    'homepage.apps.HomepageConfig',
    'feedback.apps.FeedbackConfig',
    'rating.apps.RatingConfig',
    'authorisation.apps.AuthorisationConfig',
    'django_cleanup.apps.CleanupConfig',
]

FOREIGN_APPS = [
    'sorl.thumbnail',
    'ckeditor',
]

INSTALLED_APPS += CUSTOM_APPS
INSTALLED_APPS += FOREIGN_APPS


# --------------------------------------------------------------------
# --------------------------Middleware Section------------------------
# --------------------------------------------------------------------

MIDDLEWARE: List[str] = []

COMMON_MIDDLEWARES: List[str] = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

OTHER_MIDDLEWARES: List[str] = [
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

if DEBUG:
    OTHER_MIDDLEWARES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    INSTALLED_APPS += ('debug_toolbar',)
    INTERNAL_IPS = [
        '127.0.0.1',
    ]

if REVERSER_MIDDLEWARE:
    OTHER_MIDDLEWARES += ('lyceum.middlewares.CoffeeTime',)

REVERSER_MIDDLEWARE_ENABLE = 10

MIDDLEWARE += COMMON_MIDDLEWARES
MIDDLEWARE += OTHER_MIDDLEWARES

ROOT_URLCONF: str = 'lyceum.urls'

# -----------------------------------------------------------------------
# ---------------------------Templates Section---------------------------
# -----------------------------------------------------------------------

TEMPLATES: List[Dict[str, Any]] = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'lyceum.context_processors.today_birthday_processor',
            ],
        },
    },
]

WSGI_APPLICATION: str = 'lyceum.wsgi.application'

# -----------------------------------------------------------------------
# ----------------------------Database Section---------------------------
# -----------------------------------------------------------------------

DATABASES: Dict[str, Dict[str, Union[str, Path]]] = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# -----------------------------------------------------------------------
# --------------------------USER AUTH Section----------------------------
# -----------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS: List[Dict[str, str]] = [
    {
        'NAME': 'django.contrib.auth.password_validation.'
        + 'UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
        + 'MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
        + 'CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
        + 'NumericPasswordValidator',
    },
]

AUTHENTICATION_BACKENDS = ['lyceum.backends.LoginBackend']

FAILED_AUTHS_TO_DEACTIVATE = int(os.getenv('FAILED_AUTHS_TO_DEACTIVATE', '10'))

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/auth/login/'
LOGOUT_REDIRECT_URL = '/auth/login/'

NEW_USERS_ACTIVATED = DEBUG or os.getenv(
    'NEW_USERS_ACTIVATED', 'False'
).lower() in (
    'true',
    '1',
    't',
)

ACTIVATION_URL_EXPIRE_TIME = os.getenv(
    'ACTIVATION_URL_EXPIRE_TIME', '00 12:00:00'
)

# -----------------------------------------------------------------------
# -------------------------Client settings Section-----------------------
# -----------------------------------------------------------------------

LANGUAGE_CODE: str = 'ru'

TIME_ZONE: str = 'Europe/Moscow'

USE_I18N: bool = True

USE_L10N: bool = True

USE_TZ: bool = True

# -----------------------------------------------------------------------
# ----------------------Static/Media Files Section-----------------------
# -----------------------------------------------------------------------

STATIC_URL: str = '/static/'

STATICFILES_DIR_DEV = BASE_DIR / 'static_dev'

STATICFILES_DIRS = [
    STATICFILES_DIR_DEV,
]


MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

# --------------------------------------------------------------------
# --------------------------locale Section----------------------------
# --------------------------------------------------------------------

LOCALE = 'ru'
LOCALE_FALLBACK = 'en'
LOCALES = ('ru', 'en')
LOCALES_PATH = BASE_DIR / 'locale'
LOCALE_PATHS = (BASE_DIR / 'locale',)

LANGUAGES = (
    ('ru', _('Russian')),
    ('en', _('English')),
)

# -----------------------------------------------------------------------
# --------------------------------EMAIL----------------------------------
# -----------------------------------------------------------------------

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'

EMAIL_FILE_PATH = BASE_DIR / 'send_email'

FEEDBACK_URL = 'uploads/feedback/'  # by media root

# -----------------------------------------------------------------------
# ------------------------------Plugins----------------------------------
# -----------------------------------------------------------------------

CKEDITOR_BASEPATH = STATIC_URL + 'ckeditor/ckeditor/'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Italic', 'Underline'],
            [
                'NumberedList',
                'BulletedList',
                '-',
                'Outdent',
                'Indent',
                '-',
                'JustifyLeft',
                'JustifyCenter',
                'JustifyRight',
                'JustifyBlock',
            ],
            ['Link', 'Unlink'],
            ['RemoveFormat', 'Source'],
        ],
    }
}
CKEDITOR_UPLOAD_PATH = 'ckeditor_uploads/'

# -----------------------------------------------------------------------
# ------------------------------Other Section----------------------------
# -----------------------------------------------------------------------

DEFAULT_AUTO_FIELD: str = 'django.db.models.BigAutoField'
