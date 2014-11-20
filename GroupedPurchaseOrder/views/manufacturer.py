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
from django.db.models import Q
from django.forms import ModelForm, Form, CharField
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.views.generic import ListView
from django.views.generic.edit import FormMixin

####################################################################################################

from GroupedPurchaseOrder.models import Manufacturer, Product

####################################################################################################

class ManufacturerForm(ModelForm):

    class Meta:
        model = Manufacturer
        fields = '__all__'
        # 'name',
        # 'url',
        exclude = ('creation_date',)
        # localized_fields = ('', )

    ##############################################

    def __init__(self, *args, **kwargs):

        super(ManufacturerForm, self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['autofocus'] = 'autofocus'

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

####################################################################################################

class ManufacturerSearchForm(Form):

    name = CharField(label=_('Name'), required=False, initial='')

    ##############################################

    def filter_by(self):
        return {'name__icontains': self.cleaned_data['name']}

####################################################################################################

class ManufacturerListView(FormMixin, ListView):

    model = Manufacturer
    template_name = 'GroupedPurchaseOrder/manufacturer/index.html'
    context_object_name = 'manufacturers'
    queryset = Manufacturer.objects.all().order_by('name')
    paginate_by = 25
    form_class = ManufacturerSearchForm

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

# @login_required
# def details(request, manufacturer_id):

#     manufacturer = get_object_or_404(Manufacturer, pk=manufacturer_id)

#     return render_to_response('GroupedPurchaseOrder/manufacturer/details.html',
#                               {'manufacturer': manufacturer},
#                               context_instance=RequestContext(request))

####################################################################################################

class ProductSearchForm(Form):

    keywords = CharField(label=_('Name'), required=False, initial='')

    ##############################################

    def filter_by(self):
        # return {'name__icontains': self.cleaned_data['keywords']}
        keywords = self.cleaned_data['keywords']
        return (Q(name__icontains=keywords) |
                Q(description__icontains=keywords) |
                Q(part_number__icontains=keywords))

####################################################################################################

class ManufacturerCatalogListView(FormMixin, ListView):

    model = Product
    template_name = 'GroupedPurchaseOrder/manufacturer/details.html'
    context_object_name = 'products'
    paginate_by = 25
    form_class = ProductSearchForm

    ##############################################

    def get_form_kwargs(self):
        # Called by self.get_form
        return {'initial': self.get_initial(),
                'prefix': self.get_prefix(),
                'data': self.request.GET or None}

    ##############################################

    def get(self, request, manufacturer_id, *args, **kwargs):

        manufacturer = get_object_or_404(Manufacturer, pk=manufacturer_id)

        self.object_list = manufacturer.product_set.all().order_by('name')

        form = self.get_form(self.get_form_class())
        if form.is_valid():
            self.object_list = self.object_list.filter(form.filter_by()) # **
            keywords_query = form.cleaned_data['keywords']
            query = '&keywords=' + keywords_query # Fixme: escape
        else:
            query = ''
        print(form.is_valid(), query)

        # allow_empty = self.get_allow_empty() # assumed to be True
        context = self.get_context_data(form=form, query=query, manufacturer=manufacturer)
        return self.render_to_response(context)

####################################################################################################

@login_required
def create(request):

    if request.method == 'POST':
        form = ManufacturerForm(request.POST)
        if form.is_valid():
            manufacturer = form.save(commit=False)
            manufacturer.save()
            messages.success(request, _('Manufacturer successfully created.'))
            return HttpResponseRedirect(reverse('manufacturers.details', args=[manufacturer.pk]))
        else:
            messages.error(request, _("Some information are missing or mistyped"))
    else:
        form = ManufacturerForm()

    return render_to_response('GroupedPurchaseOrder/manufacturer/create.html',
                              {'form': form},
                              context_instance=RequestContext(request))

####################################################################################################

@login_required
def update(request, manufacturer_id):

    manufacturer = get_object_or_404(Manufacturer, pk=manufacturer_id)

    if request.method == 'POST':
        form = ManufacturerForm(request.POST, instance=manufacturer)
        if form.is_valid():
            manufacturer = form.save()
            return HttpResponseRedirect(reverse('manufacturers.details', args=[manufacturer.pk]))
    else:
        form = ManufacturerForm(instance=manufacturer)

    return render_to_response('GroupedPurchaseOrder/manufacturer/create.html',
                              {'form': form, 'update': True, 'manufacturer': manufacturer},
                              context_instance=RequestContext(request))

####################################################################################################

@login_required
def delete(request, manufacturer_id):

    manufacturer = get_object_or_404(Manufacturer, pk=manufacturer_id)
    messages.success(request, _("«%(name)s» deleted") % ({'name': manufacturer.name}))
    manufacturer.delete()

    return HttpResponseRedirect(reverse('manufacturers.index'))

####################################################################################################
# 
# End
# 
####################################################################################################
