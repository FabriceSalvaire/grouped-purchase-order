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

import binascii
import os
import pytz

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext

####################################################################################################

from .settings import LANGUAGES

####################################################################################################

def random_hash():
    """ Create a random string of size 30 """
    return binascii.b2a_hex(os.urandom(15))

####################################################################################################

def all_timezones():
    return [(tz, tz) for tz in pytz.all_timezones]

####################################################################################################

class Profile(models.Model):

    class Meta:
        app_label = 'GroupedPurchaseOrder'

    # http:// /doc/ref/contrib/auth.html#django.contrib.auth.models.User
    user = models.OneToOneField(User)
    phone_number = models.CharField(max_length=30, blank=True, null=True)
    # hash_id is used to confirm the profile
    hash_id = models.CharField(unique=True, max_length=30, default=random_hash)
    language = models.CharField(max_length=4, blank=True, null=True, choices=LANGUAGES)
    timezone = models.CharField(max_length=40, choices=all_timezones(), default='UTC')

    ##############################################

    def clean(self):

        if self.timezone == 'UTC':
            # Fixme: dict?
            raise ValidationError({'timezone': [ugettext('UTC is not valid timezone')]})

    ##############################################

    def __str__(self):
        return "{}".format(self.user)

####################################################################################################
# 
# End
# 
####################################################################################################
