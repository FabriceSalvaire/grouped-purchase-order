####################################################################################################
# 
# GroupedPurchaseOrder - A Django Application.
# Copyright (C) 2014 Fabrice Salvaire
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
# 
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
# 
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
####################################################################################################

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

####################################################################################################

"""
Django settings for GroupedPurchaseOrder project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

####################################################################################################

import os

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

####################################################################################################
#
# Debug
#

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
#DEBUG = False

TEMPLATE_DEBUG = True

TASTYPIE_FULL_DEBUG = True

# Log email on console
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

####################################################################################################

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

####################################################################################################

ROOT_URLCONF = 'mysite.urls'

WSGI_APPLICATION = 'mysite.wsgi.application'

ALLOWED_HOSTS = ['localhost']
SITE_ID = 1
DEFAULT_FROM_EMAIL = 'fabrice.salvaire@orange.fr'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&z*c()=5e#jjkml#n%wx^))lkz16kwluu@tnqi5f(2!5e!vq^f'

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)

FIXTURE_DIR = 'fixtures'
# python manage.py collectstatic
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates'),
                 # Fixme: for notification
                 os.path.join(BASE_DIR, 'GroupedPurchaseOrder', 'templates', 'GroupedPurchaseOrder')]

####################################################################################################
#
# Database
#   https://docs.djangoproject.com/en/1.7/ref/settings/#databases
#

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

####################################################################################################
#
# Application definition
#

INSTALLED_APPS = (
    # /!\ ordered list
    # 'django.contrib.admindocs',
    'django.contrib.sites',
    # 'django_admin_bootstrapped.bootstrap3', # before admin
    # 'django_admin_bootstrapped', # before admin
    'suit', # before admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    # 'django_bootstrap_breadcrumbs',
    'tastypie',
    'django_ajax',
    'djangular',
    'notification',
    'django_messages',
    'GroupedPurchaseOrder',
)

MIDDLEWARE_CLASSES = (
    # /!\ ordered list
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware', # require session
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django_messages.context_processors.inbox',
)

####################################################################################################
#
# Internationalization
#   https://docs.djangoproject.com/en/1.7/topics/i18n/
#

# LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'UTC'
TIME_ZONE = 'Europe/Paris'
LANGUAGE_CODE = 'fr'
USE_I18N = True
USE_L10N = True
USE_TZ = True

####################################################################################################
#
# Django Suit configuration
#

SUIT_CONFIG = {
    # header
    'ADMIN_NAME': 'G.P.O.',
    # 'HEADER_DATE_FORMAT': 'l, j. F Y',
    # 'HEADER_TIME_FORMAT': 'H:i',

    # forms
    'SHOW_REQUIRED_ASTERISK': True,  # Default True
    # 'CONFIRM_UNSAVED_CHANGES': True, # Default True

    # menu
    # 'SEARCH_URL': '/admin/auth/user/',
    # 'MENU_ICONS': {
    #    'sites': 'icon-leaf',
    #    'auth': 'icon-lock',
    # },
    # 'MENU_OPEN_FIRST_CHILD': True, # Default True
    # 'MENU_EXCLUDE': ('auth.group',),
    # 'MENU': (
    #     'sites',
    #     {'app': 'auth', 'icon':'icon-lock', 'models': ('user', 'group')},
    #     {'label': 'Settings', 'icon':'icon-cog', 'models': ('auth.user', 'auth.group')},
    #     {'label': 'Support', 'icon':'icon-question-sign', 'url': '/support/'},
    # ),

    # misc
    # 'LIST_PER_PAGE': 15
}

####################################################################################################
# 
# End
# 
####################################################################################################
