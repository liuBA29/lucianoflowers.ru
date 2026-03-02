# mypy: ignore-errors
# flake8: noqa
from .base import *
from django.utils.translation import ugettext_lazy as _


DEBUG = True

BASE_URL = 'http://stroykerbox.local'

RQ_PERIODIC = []

INVOICE_CSS_PATH = path('static', 'css', 'style.css')

ADMIN__PRODUCT_PER_PAGE = 10
# INTERNAL_IPS = ['*',]

INSTALLED_APPS += [
    'django.contrib.redirects',
    # 'stroykerbox.apps.smartlombard',
    # 'stroykerbox.apps.booking',
    # 'stroykerbox.apps.vk_market',
]

# MIDDLEWARE += ['django.contrib.redirects.middleware.RedirectFallbackMiddleware']
MIDDLEWARE += ['stroykerbox.apps.utils.middleware.CustomRedirectFallbackMiddleware']


ALLOWED_HOSTS = ['*', '127.0.0.1', 'stroykerbox.local']

if DEBUG:
    import os  # only if you haven't already imported this
    import socket  # only if you haven't already imported this

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + [
        "127.0.0.1",
        "10.0.2.2",
    ]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'stroykerbox',
        'USER': 'stroykerbox',
        'PASSWORD': 'stroykerbox',
        'HOST': 'pg',  # db service name in the docker-compose.yml
        'PORT': '5432',
    }
}


DEBUG_TOOLBAR_CONFIG = {
    # Toolbar options
    "SHOW_TOOLBAR_CALLBACK": lambda x: True,
    # 'RESULTS_CACHE_SIZE': 3,
    'SHOW_COLLAPSED': True,
    # Panel options
    'SQL_WARNING_THRESHOLD': 100,  # milliseconds
    'SHOW_TEMPLATE_CONTEXT': True,
}

LOGGING['loggers']['catalog.moy_sklad.sync'] = {  # typing: ignore
    'handlers': ['console'],
    'level': 'DEBUG',
    'propagate': False,
}

EMAIL_FILE_PATH = path('test_email')
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'

RECAPTCHA_TESTING = True
RECAPTCHA_PRIVATE_KEY = RECAPTCHA_PUBLIC_KEY = ''
SILENCED_SYSTEM_CHECKS = ['django_recaptcha.recaptcha_test_key_error']

SHELL_PLUS_IMPORTS = [
    # 'from stroykerbox.apps.vk_market.vk import VKMarket',
    # 'from stroykerbox.apps.novofon.helper import Novofon',
    # 'from stroykerbox.apps.floatprice import tasks as fp_tasks',
    'from stroykerbox.apps.amocrm import amocrm as amo',
    # 'from stroykerbox.apps.common.services import FrontpageParser, CommonChecker',
    'from constance import config',
    # 'from stroykerbox.apps.smartlombard.tbank.services.smartlombard_api import SmartlombardAPI',
    # 'from stroykerbox.apps.smartlombard.tbank.services.tbank_api import TBankAPI',
    'from stroykerbox.apps.crm.tasks import process_new_callme_request, process_new_feedback_message_request',
]
