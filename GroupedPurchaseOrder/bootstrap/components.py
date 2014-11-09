####################################################################################################
# 
# @Project@ - @ProjectDescription@.
# Copyright (C) 2014 Fabrice Salvaire
# 
####################################################################################################

####################################################################################################

from django.forms.utils import flatatt
from django.utils.html import format_html, format_html_join
from django.utils.safestring import mark_safe

####################################################################################################

def render_icon(icon, title=''):

    """Render a glyphicon.

    """

    # attrs = {'class': 'glyphicon glyphicon-{}'.format(icon)}
    attrs = {'class': 'glyphicon glyphicon-' + icon}
    if title:
        attrs['title'] = title
    return format_html('<span{0}></span>', flatatt(attrs))

####################################################################################################
# 
# End
# 
####################################################################################################
