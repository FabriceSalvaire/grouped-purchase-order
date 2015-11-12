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

from django import template

####################################################################################################

from GroupedPurchaseOrder.bootstrap.components import (render_icon,
                                                       render_button, render_icon_button,
                                                       render_modal_icon_button, render_dismiss_button,
                                                       render_close_button)

####################################################################################################

register = template.Library()

####################################################################################################

register.simple_tag(render_icon, name='bootstrap_icon')
register.simple_tag(render_button, name='bootstrap_button')
register.simple_tag(render_icon_button, name='bootstrap_icon_button')
register.simple_tag(render_modal_icon_button, name='bootstrap_modal_icon_button')
register.simple_tag(render_dismiss_button, name='bootstrap_dismiss_button')
register.simple_tag(render_close_button, name='bootstrap_close_button')

# Add icon_link
# <a href="{{ supplier.url }}">{% bootstrap_icon 'home' %}</a>
# {% bootstrap_icon_link 'home' supplier.url %}

####################################################################################################
# 
# End
# 
####################################################################################################
