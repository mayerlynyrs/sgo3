"""Development settings."""

from .base import *  # NOQA
from .base import env

# Base
DEBUG = True

X_FRAME_OPTIONS = 'SAMEORIGIN'

XS_SHARING_ALLOWED_METHODS = ['POST','GET','OPTIONS', 'PUT', 'DELETE']

# Security
SECRET_KEY = env('DJANGO_SECRET_KEY', default='SppX+BTNkUqWd2zAtIpgf3c5w0ExH1ELaL30QP+GBCPebtPzT9kSMmRT5Q5JXj2LIC5R3CgpF0y5fI6oJHEmtw')
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default=['localhost'])
ALLOWED_HOSTS += [
    "localhost",
    "0.0.0.0",
    "127.0.0.1",
    "192.168.0.51", #nico
    "192.168.0.201", #maye
    "192.168.0.93", #server
]

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
    }
}

# Templates
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG  # NOQA

# Email
EMAIL_USE_TLS = True
EMAIL_HOST = 'arrow.direcnode.com'
EMAIL_HOST_USER = 'notificaciones@empresasintegra.cl'
EMAIL_HOST_PASSWORD = 'integra*#notificaciones2022'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_PORT = 587
# django-extensions
INSTALLED_APPS += ['django_extensions']  # noqa F405

# django CROS
CORS_ORIGIN_WHITELIST = [
    "http://localhost:4200", # angular
]
