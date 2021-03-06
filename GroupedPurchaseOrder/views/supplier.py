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
from django.forms import ModelForm, Form, CharField
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.views.generic.list import ListView
from django.views.generic.edit import FormMixin

####################################################################################################

from GroupedPurchaseOrder.models import Supplier

####################################################################################################

class SupplierForm(ModelForm):

    class Meta:
        model = Supplier
        fields = '__all__'
        # 'name',
        # 'url',
        # 'purchase_therms_url',
        # 'delivery_therms_url',
        # 'description',
        # 'minimum_purchase',
        # 'free_shipment_threshold',
        exclude = ('creation_date',)
        # localized_fields = ('', )

    ##############################################

    def __init__(self, *args, **kwargs):

        super(SupplierForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['autofocus'] = 'autofocus'

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

####################################################################################################

class SupplierSearchForm(Form):

    name = CharField(label=_('Name'), required=False, initial='')

    ##############################################

    def filter_by(self):
        return {'name__icontains': self.cleaned_data['name']}

####################################################################################################

class SupplierListView(FormMixin, ListView):

    model = Supplier
    template_name = 'GroupedPurchaseOrder/supplier/index.html'
    context_object_name = 'suppliers'
    queryset = Supplier.objects.all().order_by('name')
    paginate_by = 25
    form_class = SupplierSearchForm

    ##############################################

    def get_form_kwargs(self):
        # Called by self.get_form
        return {'initial': self.get_initial(),
                'prefix': self.get_prefix(),
                'data': self.request.GET or None}

    ##############################################

    def get(self, request, *args, **kwargs):

        self.object_list = self.get_queryset()

        form = self.get_form(self.get_form_class())
        if form.is_valid():
            self.object_list = self.object_list.filter(**form.filter_by())
            name_query = form.cleaned_data['name']
            query = '&name=' + name_query # Fixme: escape
        else:
            query = ''

        # allow_empty = self.get_allow_empty() # assumed to be True
        context = self.get_context_data(form=form, query=query)
        return self.render_to_response(context)

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

@login_required
def catalog(request, supplier_id):

    supplier = get_object_or_404(Supplier, pk=supplier_id)

    return render_to_response('GroupedPurchaseOrder/supplier/catalog.html',
                              {'supplier': supplier},
                              context_instance=RequestContext(request))

####################################################################################################
# 
# End
# 
####################################################################################################
