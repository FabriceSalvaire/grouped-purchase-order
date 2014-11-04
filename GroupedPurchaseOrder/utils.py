####################################################################################################
# 
# GroupedPurchaseOrder - A Django Application.
# Copyright (C) 2014 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
####################################################################################################

####################################################################################################

import logging
import pytz

####################################################################################################

from django.conf import settings
from django.core.mail import send_mail
from django.template import loader
from django.utils import timezone as dj_timezone
from django.utils import translation as dj_translation

####################################################################################################

logger = logging.getLogger('gpo.utils')

####################################################################################################

class Localize(object):

    ##############################################
    
    def __init__(self, language, timezone):

        self._language = language
        self._timezone = timezone

    ##############################################

    def __enter__(self):

        if self._language:
            dj_translation.activate(self._language)
        if self._timezone:
            dj_timezone.activate(pytz.timezone(self._timezone))

    ##############################################

    def __exit__(self, type_name, value, traceback):

        if self._timezone:
            dj_timezone.deactivate()
        if self._language:
            dj_translation.deactivate()

####################################################################################################

def send_mail_help(user, subject, template_name, ctx):

    body = loader.render_to_string(template_name, ctx)
    logger.info("Sending email to '%s' ('%s')",
                user.get_full_name(), user.email, extra={'data': ctx})
    send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [user.email])

####################################################################################################

def send_localized_mail(user, subject, template_name, ctx):

    with Localize(user.profile.language, user.profile.timezone):
        send_mail_help(user, subject, template_name, ctx)

####################################################################################################
# 
# End
# 
####################################################################################################
