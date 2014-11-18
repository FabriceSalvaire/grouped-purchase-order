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

from GroupedPurchaseOrder.models import ProductOrder, SupplierProduct

####################################################################################################

class ProductOrderForm(ModelForm):

    class Meta:
        model = ProductOrder
        fields = '__all__'
        exclude = ('creation_date',)
        # localized_fields = ('', )

    ##############################################

    def __init__(self, *args, **kwargs):

        super(ProductOrderForm, self).__init__(*args, **kwargs)

        # self.fields['name'].widget.attrs['autofocus'] = 'autofocus'

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

####################################################################################################

@login_required
def details(request, product_order_id):

    product_order = get_object_or_404(ProductOrder, pk=product_order_id)
    return render_to_response('GroupedPurchaseOrder/product_order/details.html',
                              {'product_order': product_order},
                              context_instance=RequestContext(request))

####################################################################################################

@login_required
def create(request, supplier_product_id):

    # http_referer = request.META['HTTP_REFERER']
    # print(http_referer)

    if request.method == 'POST':
        form = ProductOrderForm(request.POST)
        if form.is_valid():
            product_order = form.save(commit=False)
            product_order.save()
            messages.success(request, _('ProductOrder successfully created.'))
            product_order_url = reverse('product_orders.details', args=[product_order.pk])
            order_url = reverse('orders.details', args=[product_order.user_order.order.pk])
            return HttpResponseRedirect(order_url)
        else:
            messages.error(request, _("Some information are missing or mistyped"))
    else:
        if supplier_product_id is not None:
            supplier_product = SupplierProduct.objects.get(pk=supplier_product_id)
            order = supplier_product.supplier.new_order()
            user_order = order.user_order(request.user)
            initial_data = {'user_order': user_order,
                            'supplier_product': supplier_product_id}
        else:
            initial_data = {}
        form = ProductOrderForm(initial=initial_data)

    return render_to_response('GroupedPurchaseOrder/product_order/create.html',
                              {'form': form},
                              context_instance=RequestContext(request))

####################################################################################################

@login_required
def update(request, product_order_id=None):

    product_order = get_object_or_404(ProductOrder, pk=product_order_id)

    if request.method == 'POST':
        form = ProductOrderForm(request.POST, instance=product_order)
        if form.is_valid():
            product_order = form.save()
            return HttpResponseRedirect(reverse('product_orders.details', args=[product_order.pk]))
    else:
        form = ProductOrderForm(instance=product_order)

    return render_to_response('GroupedPurchaseOrder/product_order/create.html',
                              {'form': form, 'update': True, 'product_order': product_order},
                              context_instance=RequestContext(request))

####################################################################################################

@login_required
def delete(request, product_order_id):

    product_order = get_object_or_404(ProductOrder, pk=product_order_id)
    order = product_order.user_order.order
    messages.success(request, _("«%(name)s» deleted") % ({'name': product_order.name()}))
    product_order.delete()

    return HttpResponseRedirect(reverse('orders.details', args=[order.pk]))

####################################################################################################
# 
# End
# 
####################################################################################################
