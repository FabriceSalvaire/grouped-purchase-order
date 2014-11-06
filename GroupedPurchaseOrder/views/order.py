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

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.views.generic.list import ListView

####################################################################################################

from GroupedPurchaseOrder.models import Order

####################################################################################################

class OrderForm(ModelForm):

    class Meta:
        model = Order
        fields = '__all__'
        exclude = ('creation_date',)
        # localized_fields = ('', )

    ##############################################

    def __init__(self, *args, **kwargs):

        super(OrderForm, self).__init__(*args, **kwargs)

        # self.fields['name'].widget.attrs['autofocus'] = 'autofocus'

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

####################################################################################################

class OrderListView(ListView):

    model = Order
    template_name = 'GroupedPurchaseOrder/order/index.html'
    context_object_name = 'orders'

####################################################################################################

@login_required
def details(request, order_id):

    order = get_object_or_404(Order, pk=order_id)

    return render_to_response('GroupedPurchaseOrder/order/details.html',
                              {'order': order},
                              context_instance=RequestContext(request))

####################################################################################################

@login_required
def create(request):

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.save()
            messages.success(request, _('Order successfully created.'))
            return HttpResponseRedirect(reverse('orders.details', args=[order.pk]))
        else:
            messages.error(request, _("Some information are missing or mistyped"))
    else:
        form = OrderForm()

    return render_to_response('GroupedPurchaseOrder/order/create.html',
                              {'form': form},
                              context_instance=RequestContext(request))

####################################################################################################

@login_required
def update(request, order_id):

    order = get_object_or_404(Order, pk=order_id)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save()
            return HttpResponseRedirect(reverse('orders.details', args=[order.pk]))
    else:
        form = OrderForm(instance=order)

    return render_to_response('GroupedPurchaseOrder/order/create.html',
                              {'form': form, 'update': True, 'order': order},
                              context_instance=RequestContext(request))

####################################################################################################

@login_required
def delete(request, order_id):

    order = get_object_or_404(Order, pk=order_id)
    messages.success(request, _("«%(name)s» deleted") % ({'name': order.name}))
    order.delete()

    return HttpResponseRedirect(reverse('orders.index'))

####################################################################################################
# 
# End
# 
####################################################################################################
