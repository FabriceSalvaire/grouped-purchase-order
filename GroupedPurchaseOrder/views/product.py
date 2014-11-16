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

from GroupedPurchaseOrder.models import Product, Manufacturer

####################################################################################################

class ProductForm(ModelForm):

    class Meta:
        model = Product
        fields = '__all__'
        # 'name',
        # 'url',
        exclude = ('creation_date',)
        # localized_fields = ('', )

    ##############################################

    def __init__(self, *args, **kwargs):

        super(ProductForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['autofocus'] = 'autofocus'

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

####################################################################################################

@login_required
def details(request, product_id):

    product = get_object_or_404(Product, pk=product_id)

    return render_to_response('GroupedPurchaseOrder/product/details.html',
                              {'product': product},
                              context_instance=RequestContext(request))

####################################################################################################

@login_required
def create(request, manufacturer_id=None):

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            messages.success(request, _('Product successfully created.'))
            return HttpResponseRedirect(reverse('products.details', args=[product.pk]))
        else:
            messages.error(request, _("Some information are missing or mistyped"))
    else:
        if manufacturer_id is not None:
            initial_data = {'manufacturer': manufacturer_id}
            manufacturer = Manufacturer.objects.get(pk=manufacturer_id)
        else:
            initial_data = {}
            manufacturer = None
        form = ProductForm(initial=initial_data)

    return render_to_response('GroupedPurchaseOrder/product/create.html',
                              {'form': form,
                               'manufacturer': manufacturer},
                              context_instance=RequestContext(request))

####################################################################################################

@login_required
def update(request, product_id):

    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save()
            return HttpResponseRedirect(reverse('products.details', args=[product.pk]))
    else:
        form = ProductForm(instance=product)

    return render_to_response('GroupedPurchaseOrder/product/create.html',
                              {'form': form, 'update': True, 'product': product},
                              context_instance=RequestContext(request))

####################################################################################################

@login_required
def delete(request, product_id):

    product = get_object_or_404(Product, pk=product_id)
    messages.success(request, _("«%(name)s» deleted") % ({'name': product.name}))
    product.delete()

    return HttpResponseRedirect(reverse('products.index'))

####################################################################################################
# 
# End
# 
####################################################################################################
