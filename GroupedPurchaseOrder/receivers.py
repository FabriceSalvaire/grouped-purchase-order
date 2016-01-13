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

####################################################################################################

from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.db import models
from django.dispatch import receiver

####################################################################################################

from tastypie.models import create_api_key

####################################################################################################

# @receiver(user_logged_in)
# def set_profile_info(sender, **kwargs):

#     """ Set language and timezone if defined in the profile """

#     language = kwargs['user'].profile.language
#     if language:
#         kwargs['request'].session['django_language'] = language

#     tz = kwargs['user'].profile.timezone
#     if tz:
#         kwargs['request'].session['django_timezone'] = tz

models.signals.post_save.connect(create_api_key, sender=User)

####################################################################################################
#
# End
#
####################################################################################################
