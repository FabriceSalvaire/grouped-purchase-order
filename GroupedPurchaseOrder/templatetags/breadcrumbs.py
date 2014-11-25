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
#
# Forked from https://github.com/prymitive/bootstrap-breadcrumbs
# Copyright 2013 by Łukasz Mierzwa
#   l.mierzwa@gmail.com
#
# Modifications:
#  - fixed leading space in the template
#  - Python3/Djano 1.7 only
#  - code cleanup
#
# Fixme:
#  - how to store user data: META, render_context ?
#  - any API to parse args, kwargs ?
#
####################################################################################################

####################################################################################################

from inspect import ismethod
import logging

####################################################################################################

# from django.utils.encoding import smart_text
from django import template
from django.core.urlresolvers import reverse, NoReverseMatch
from django.db.models import Model
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

####################################################################################################

_module_logger = logging.getLogger(__name__)

####################################################################################################

register = template.Library()

####################################################################################################

_CONTEXT_KEY = 'breadcrumb_links'

####################################################################################################

def _check_context_as_request(context):

    if 'request' not in context:
        raise NameError("request object not found in context!"
                        "Check if 'django.core.context_processors.request' is in TEMPLATE_CONTEXT_PROCESSORS")

####################################################################################################

def _append_breadcrumb(context, label, viewname, args, kwargs):

    # _check_context_as_request(context)
    # meta = context['request'].META
    # breadcrumbs = meta.setdefault(_CONTEXT_KEY, [])
    meta = context.render_context
    if _CONTEXT_KEY not in meta:
        meta[_CONTEXT_KEY] = []
    breadcrumbs = meta[_CONTEXT_KEY]
    breadcrumbs.append((label, viewname, args, kwargs))

####################################################################################################

@register.simple_tag(takes_context=True)
def clear_breadcrumbs(context, *args):

    """Clear the breadcrumbs.

    """

    # _check_context_as_request(context)
    # meta = context['request'].META
    meta = context.render_context
    if _CONTEXT_KEY in meta:
        del meta[_CONTEXT_KEY]

    return ''

####################################################################################################

@register.simple_tag(takes_context=True)
def breadcrumb(context, label, viewname, *args, **kwargs):
    """
    Add link to list of breadcrumbs, usage:

    {% load breadcrumbs %}
    {% breadcrumb "Home" "index" %}

    Remember to use it inside {% block %} with {{ block.super }} to get all parent breadcrumbs.

    label: Breadcrumb link label.
    viewname: Name of the view to link this breadcrumb to, or Model instance with implemented get_absolute_url().
    args kwargs: Any arguments to view function.
    """
    _append_breadcrumb(context, _(escape(label)), viewname, args, kwargs)
    return ''

####################################################################################################

@register.simple_tag(takes_context=True)
def breadcrumb_safe(context, label, viewname, *args, **kwargs):
    """
    Same as breadcrumb but label is not escaped.
    """
    _append_breadcrumb(context, _(label), viewname, args, kwargs)
    return ''

####################################################################################################

@register.simple_tag(takes_context=True)
def breadcrumb_raw(context, label, viewname, *args, **kwargs):
    """
    Same as breadcrumb but label is not translated.
    """
    _append_breadcrumb(context, escape(label), viewname, args, kwargs)
    return ''

####################################################################################################

@register.simple_tag(takes_context=True)
def breadcrumb_raw_safe(context, label, viewname, *args, **kwargs):
    """
    Same as breadcrumb but label is not escaped and translated.
    """
    _append_breadcrumb(context, label, viewname, args, kwargs)
    return ''

####################################################################################################

@register.simple_tag(takes_context=True)
def render_breadcrumbs(context, *args):

    """
    Render breadcrumbs using Bootstrap.
    """

    if args:
        template_path = args[0]
    else:
        template_path = 'GroupedPurchaseOrder/breadcrumbs.html'

    # _check_context_as_request(context)
    # meta = context['request'].META
    meta = context.render_context
    breadcrumbs = meta.get(_CONTEXT_KEY, [])
    # print(breadcrumbs)
    links = []
    for label, viewname, view_args, view_kwargs in breadcrumbs:
        if (isinstance(viewname, Model) and
            hasattr(viewname, 'get_absolute_url') and
            ismethod(viewname.get_absolute_url)):
            url = viewname.get_absolute_url(*view_args, **view_kwargs)
        else:
            try:
                current_app = context['request'].resolver_match.namespace
                url = reverse(viewname=viewname, args=view_args, kwargs=view_kwargs, current_app=current_app)
            except NoReverseMatch:
                url = viewname
        #? smart_text(label) if label else label
        links.append((url, label))

    if not links:
        return ''
    else:
        return mark_safe(template.loader.render_to_string(template_path,
                                                          {'breadcrumbs': links,
                                                           'len_breadcrumbs': len(links)}))

####################################################################################################

class BreadcrumbNode(template.Node):

    ##############################################

    def __init__(self, nodelist, viewname, args):

        self._nodelist = nodelist
        self._viewname = viewname

        #? Any API to do that?
        self._args = []
        self._kwargs = {}
        for arg in args:
            if '=' in arg:
                name, value = arg.split('=') #? must check name and value
                self._kwargs[name] = value
            else:
                self._args.append(arg)

    ##############################################

    @staticmethod
    def _resolve_variable(context, variable):

        try:
            value = template.Variable(variable).resolve(context)
        except template.VariableDoesNotExist:
            value = variable
        return value

    ##############################################

    def render(self, context):

        label = self._nodelist.render(context)
        viewname = self._resolve_variable(context, self._viewname)
        args = [self._resolve_variable(context, arg) for arg in self._args]
        kwargs = {name:self._resolve_variable(context, value) for name, value in self._kwargs.items()}
        _append_breadcrumb(context, label, viewname, args, kwargs)
        return ''

####################################################################################################

@register.tag
def breadcrumb_for(parser, token):
    """
    {% breadcrumb_for viewname [*args] [**kwargs] %}
      ...
    {% endbreadcrumb_for %}
    """
    tokens = token.split_contents()
    viewname, args = tokens[1], tokens[2:] # args contains kwargs tokens
    nodelist = parser.parse(('endbreadcrumb_for',))
    parser.delete_first_token()
    return BreadcrumbNode(nodelist, viewname, args)

####################################################################################################
# 
# End
# 
####################################################################################################
