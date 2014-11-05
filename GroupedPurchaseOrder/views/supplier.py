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

from GroupedPurchaseOrder.models import Supplier

####################################################################################################

class SupplierForm(ModelForm):

    class Meta:
        model = Supplier
        fields = (
            # 'creation_date',
            'name',
            'url',
            'purchase_therms_url',
            'delivery_therms_url',
            'description',
            'minimum_purchase',
            'free_shipment_threshold',
        )
        # localized_fields = ('', )

    ##############################################

    def __init__(self, *args, **kwargs):

        super(SupplierForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['autofocus'] = 'autofocus'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['placeholder'] = _('Description')

####################################################################################################

class SupplierListView(ListView):

    model = Supplier
    template_name = 'GroupedPurchaseOrder/supplier/index.html'
    context_object_name = 'suppliers'

####################################################################################################

@login_required
def details(request, supplier_id):

    supplier = get_object_or_404(Supplier, pk=supplier_id)

    return render_to_response('GroupedPurchaseOrder/supplier/details.html',
                              {'supplier': supplier},
                              context_instance=RequestContext(request))

####################################################################################################

@login_required
def create(request):

    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            supplier = form.save(commit=False)
            supplier.save()
            messages.success(request, _('Supplier successfully created.'))
            return HttpResponseRedirect(reverse('suppliers.details', args=[supplier.pk]))
        else:
            messages.error(request, _("Some information are missing or mistyped"))
    else:
        form = SupplierForm()

    return render_to_response('GroupedPurchaseOrder/supplier/create.html',
                              {'form': form},
                              context_instance=RequestContext(request))

####################################################################################################

@login_required
def update(request, supplier_id):

    supplier = get_object_or_404(Supplier, pk=supplier_id)

    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            supplier = form.save()
            return HttpResponseRedirect(reverse('suppliers.details', args=[supplier.pk]))
    else:
        form = SupplierForm(instance=supplier)

    return render_to_response('GroupedPurchaseOrder/supplier/create.html',
                              {'form': form, 'update': True, 'supplier': supplier},
                              context_instance=RequestContext(request))

####################################################################################################

@login_required
def delete(request, supplier_id):

    supplier = get_object_or_404(Supplier, pk=supplier_id)
    messages.success(request, _("«%(name)s» deleted") % ({'name': supplier.name}))
    supplier.delete()

    return HttpResponseRedirect(reverse('suppliers.index'))

####################################################################################################
# 
# End
# 
####################################################################################################
