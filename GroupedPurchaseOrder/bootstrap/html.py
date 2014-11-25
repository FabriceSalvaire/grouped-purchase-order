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

from django.forms.utils import flatatt
from django.utils.encoding import force_text as dj_force_text
from django.utils.html import format_html

####################################################################################################

def force_text(s):
    """Force a value to text, render None as an empty string.

    """
    # force_text(None) -> 'None'
    if s is None:
        return ''
    else:
        #? difference with str(s)
        return dj_force_text(s)

####################################################################################################

def join_text(args, separator=''):
    """Concatenate several values as a text string with an optional separator.

    """
    #? force_text(separator)
    return force_text(separator).join([force_text(x) for x in args if x])

####################################################################################################

def merge_new_words(string1, words2, prepend=False):
    words1 = string1.split()
    # words2 = string2.split()
    string3 = ' '.join([x for x in words2 if x not in words1])
    if prepend:
        strings = string3, string1
    else:
        strings = string1, string3
    return ' '.join(strings)

####################################################################################################

def render_tag(tag, content, attrs=None):

    """Render a HTML tag.

    """

    return format_html('<{0}{1}>{2}</{0}>',
                       tag,
                       flatatt(attrs) if attrs else '',
                       force_text(content))

####################################################################################################
# 
# End
# 
####################################################################################################
