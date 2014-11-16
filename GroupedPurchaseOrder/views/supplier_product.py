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

from GroupedPurchaseOrder.models import SupplierProduct, Supplier, Product

####################################################################################################

class SupplierProductForm(ModelForm):

    class Meta:
        model = SupplierProduct
        fields = '__all__'
        exclude = ('creation_date',)
        # localized_fields = ('', )

    ##############################################

    def __init__(self, *args, **kwargs):

        super(SupplierProductForm, self).__init__(*args, **kwargs)

        # self.fields['name'].widget.attrs['autofocus'] = 'autofocus'

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

####################################################################################################

@login_required
def details(request, supplier_product_id):

    supplier_product = get_object_or_404(SupplierProduct, pk=supplier_product_id)

    return render_to_response('GroupedPurchaseOrder/supplier_product/details.html',
                              {'supplier_product': supplier_product},
                              context_instance=RequestContext(request))

####################################################################################################

@login_required
def create(request, product_id=None):

    if request.method == 'POST':
        form = SupplierProductForm(request.POST)
        if form.is_valid():
            supplier_product = form.save(commit=False)
            supplier_product.save()
            messages.success(request, _('SupplierProduct successfully created.'))
            return HttpResponseRedirect(reverse('supplier_products.details', args=[supplier_product.pk]))
        else:
            messages.error(request, _("Some information are missing or mistyped"))
    else:
        if product_id is not None:
            initial_data = {'product': product_id}
            product = Product.objects.get(pk=product_id)
        else:
            initial_data = {}
            product = None
        form = SupplierProductForm(initial=initial_data)

    return render_to_response('GroupedPurchaseOrder/supplier_product/create.html',
                              {'form': form,
                               'product': product},
                              context_instance=RequestContext(request))

####################################################################################################

@login_required
def update(request, supplier_product_id):

    supplier_product = get_object_or_404(SupplierProduct, pk=supplier_product_id)

    if request.method == 'POST':
        form = SupplierProductForm(request.POST, instance=supplier_product)
        if form.is_valid():
            supplier_product = form.save()
            return HttpResponseRedirect(reverse('supplier_products.details', args=[supplier_product.pk]))
    else:
        form = SupplierProductForm(instance=supplier_product)

    return render_to_response('GroupedPurchaseOrder/supplier_product/create.html',
                              {'form': form,
                               'update': True,
                               'supplier_product': supplier_product,
                               'supplier':supplier_product.supplier,
                              },
                              context_instance=RequestContext(request))

####################################################################################################

@login_required
def delete(request, supplier_product_id):

    supplier_product = get_object_or_404(SupplierProduct, pk=supplier_product_id)
    messages.success(request, _("«%(name)s» deleted") % ({'name': supplier_product.name}))
    supplier_product.delete()

    return HttpResponseRedirect(reverse('supplier_products.index'))

####################################################################################################
# 
# End
# 
####################################################################################################
