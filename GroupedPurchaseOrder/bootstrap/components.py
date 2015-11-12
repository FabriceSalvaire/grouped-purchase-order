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

from django.core.urlresolvers import reverse, NoReverseMatch
from django.forms.utils import flatatt
from django.utils.html import escape, format_html
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

####################################################################################################

from .html import join_text, merge_new_words, render_tag

####################################################################################################
#
# Notes:
#  - How to concate in {% %} ? #deleteModal{{ supplier.pk }}
#  - url 'suppliers.update' supplier.pk
#
####################################################################################################

####################################################################################################

def render_icon(icon, title=''):

    """Render a glyphicon.

    """

    #? escape ?

    # attrs = {'class': 'glyphicon glyphicon-{}'.format(icon)}
    attrs = {'class': 'glyphicon glyphicon-' + icon}
    if title:
        attrs['title'] = _(title)
    return format_html('<span{0}></span>', flatatt(attrs))

####################################################################################################

def render_button(content, icon=None, style='default', size='', href='', title='', button_class='', attrs=None):
    
    """Render a button with content

    """

    # <button type="button" class="btn btn-default">Default</button>
    # <button type="button" class="btn btn-primary">Primary</button>
    # <button type="button" class="btn btn-success">Success</button>
    # <button type="button" class="btn btn-info">Info</button>
    # <button type="button" class="btn btn-warning">Warning</button>
    # <button type="button" class="btn btn-danger">Danger</button>
    # <button type="button" class="btn btn-link">Link</button>
    #
    # size : btn-lg, btn-sm, btn-xs
    # <button type="button" class="btn btn-primary btn-lg">Large button</button>
    #
    # btn-block
    # <button type="button" class="btn btn-primary btn-lg btn-block">Block level button</button>
    # <button type="button" class="btn btn-default btn-lg btn-block">Block level button</button>
    #
    # active
    # <button type="button" class="btn btn-primary btn-lg active">Primary button</button>
    # <a href="#" class="btn btn-default btn-lg active" role="button">Link</a>
    # 
    # disabled="disabled"
    # <button type="button" class="btn btn-lg btn-primary" disabled="disabled">Primary button</button>
    # <a href="#" class="btn btn-default btn-lg disabled" role="button">Link</a>
    #
    # <a class="btn btn-default" href="#" role="button">Link</a>
    # <button class="btn btn-default" type="submit">Button</button>
    # <input class="btn btn-default" type="button" value="Input">
    # <input class="btn btn-default" type="submit" value="Submit">

    if attrs is None:
        attrs = {}

    classes = ['btn']

    button_styles = ('default', 'primary', 'success', 'info', 'warning', 'danger', 'link')
    if style in button_styles:
        classes.append('btn-' + style)
    else:
        raise ValueError('Parameter style must be {} ("{}" given)',
                         ', '.join(button_styles), style)

    # size = text_value(size).lower().strip()
    if size:
        if size == 'xs':
            classes.append('btn-xs')
        elif size == 'sm' or size == 'small':
            classes.append('btn-sm')
        elif size == 'lg' or size == 'large':
            classes.append('btn-lg')
        else:
            raise ValueError('Parameter "size" should be "xs", "sm", "lg" or empty ("{}" given)',
                             format(size))

    attrs['class'] = merge_new_words(button_class, classes)

    if href:
        try:
            # current_app = context['request'].resolver_match.namespace
            # viewname=viewname, args=view_args, kwargs=view_kwargs, current_app=current_app
            url = reverse(href)
        except NoReverseMatch:
            url = href
        attrs['href'] = url
        tag = 'a'
    else:
        tag = 'button'

    if title:
        attrs['title'] = escape(_(title))

    icon_content = render_icon(icon) if icon else ''
    if content:
        content = join_text((icon_content, escape(_(content))), separator=' ')
    else:
        content = icon_content

    return render_tag(tag, mark_safe(content), attrs=attrs)

####################################################################################################

def render_icon_button(icon, **kwargs):
    return render_button(None, icon=icon, **kwargs)

####################################################################################################

def render_modal_icon_button(icon, *args, **kwargs):
    attrs = {'data-toggle':'modal', 'data-target':join_text(args)}
    return render_button(None, icon=icon, attrs=attrs, **kwargs)

####################################################################################################

def render_dismiss_button(title, **kwargs):
    attrs = {'type':'button', 'data-dismiss':'modal'}
    return render_button(title, attrs=attrs, **kwargs)

####################################################################################################

def render_close_button(*args, **kwargs):
    # '<button type="button" class="close" data-dismiss="modal">'
    # '</button>'
    attrs = {'type':'button', 'class':'close', 'data-dismiss':'modal'}
    title = escape(_('Close'))
    content = ('<span aria-hidden="true">&times;</span>'
               '<span class="sr-only">{0}</span>'.format(title))
    return render_tag('button', mark_safe(content), attrs=attrs)

####################################################################################################
# 
# End
# 
####################################################################################################
