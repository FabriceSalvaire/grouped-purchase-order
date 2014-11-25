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

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.views.generic.list import ListView

####################################################################################################

from GroupedPurchaseOrder.models import UserOrder

####################################################################################################

class UserOrderForm(ModelForm):

    class Meta:
        model = UserOrder
        fields = ('payed', 'delivery_date')
        # localized_fields = ('', )

    ##############################################

    def __init__(self, *args, **kwargs):

        super(UserOrderForm, self).__init__(*args, **kwargs)

        # self.fields['name'].widget.attrs['autofocus'] = 'autofocus'

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

####################################################################################################

class UserOrderListView(ListView):

    model = UserOrder
    template_name = 'GroupedPurchaseOrder/user_order/index.html'
    context_object_name = 'user_orders'

    ##############################################

    def get_queryset(self, profile):

        return UserOrder.objects.filter(profile=profile)

    ##############################################

    def get(self, request, *args, **kwargs):

        # Form BaseListView

        profile = request.user.profile

        self.object_list = self.get_queryset(profile)
        allow_empty = self.get_allow_empty()

        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if (self.get_paginate_by(self.object_list) is not None
                    and hasattr(self.object_list, 'exists')):
                is_empty = not self.object_list.exists()
            else:
                is_empty = len(self.object_list) == 0
            if is_empty:
                raise Http404(_("Empty list and '%(class_name)s.allow_empty' is False.")
                        % {'class_name': self.__class__.__name__})
        context = self.get_context_data()
        return self.render_to_response(context)

####################################################################################################

# @login_required
# def details(request, user_order_id):

#     user_order = get_object_or_404(UserOrder, pk=user_order_id)

#     return render_to_response('GroupedPurchaseUserOrder/user_order/details.html',
#                               {'user_order': user_order,
#                                'profile': request.user.profile},
#                               context_instance=RequestContext(request))

####################################################################################################

@login_required
def update(request, user_order_id):

    user_order = get_object_or_404(UserOrder, pk=user_order_id)

    if request.method == 'POST':
        form = UserOrderForm(request.POST, instance=user_order)
        if form.is_valid():
            user_order = form.save()
            order = user_order.order
            return HttpResponseRedirect(reverse('orders.details', args=[order.pk]))
    else:
        form = UserOrderForm(instance=user_order)

    return render_to_response('GroupedPurchaseOrder/user_order/create.html',
                              {'form': form, 'update': True, 'user_order': user_order},
                              context_instance=RequestContext(request))

####################################################################################################

# @login_required
# def delete(request, user_order_id):

#     user_order = get_object_or_404(UserOrder, pk=user_order_id)
#     messages.success(request, _("«%(name)s» deleted") % ({'name': user_order.name}))
#     user_order.delete()

#     return HttpResponseRedirect(reverse('user_orders.index'))

####################################################################################################
# 
# End
# 
####################################################################################################
