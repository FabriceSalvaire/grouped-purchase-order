####################################################################################################
# 
# @Project@ - @ProjectDescription@.
# Copyright (C) 2014 Fabrice Salvaire
# 
####################################################################################################

####################################################################################################

import logging
import pytz

####################################################################################################

from django.conf import settings
from django.core.mail import send_mail
from django.template import loader
from django.utils import timezone, translation

####################################################################################################

logger = logging.getLogger('gpo.utils')

####################################################################################################

class Localize(object):

    ##############################################
    
    def __init__(self, language, timezone):

        self.language = language
        self.timezone = timezone

    ##############################################

    def __enter__(self):

        if self.language:
            translation.activate(self.language)
        if self.timezone:
            timezone.activate(pytz.timezone(self.timezone))

    ##############################################

    def __exit__(self, type_name, value, traceback):

        if self.timezone:
            timezone.deactivate()
        if self.language:
            translation.deactivate()

####################################################################################################

def send_localized_mail(user, subject, template_name, ctx):

    with Localize(user.profile.language,
                  user.profile.timezone):
        send_mail_help(user, subject, template_name, ctx)

####################################################################################################

def send_mail_help(user, subject, template_name, ctx):

    body = loader.render_to_string(template_name, ctx)
    logger.info("Sending email to '%s' ('%s')", user.get_full_name(),
                user.email, extra={'data': ctx})
    send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [user.email])

####################################################################################################
# 
# End
# 
####################################################################################################
