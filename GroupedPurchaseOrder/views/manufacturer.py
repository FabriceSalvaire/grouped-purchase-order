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

from GroupedPurchaseOrder.models import Manufacturer

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

class ManufacturerListView(ListView):

    model = Manufacturer
    template_name = 'GroupedPurchaseOrder/manufacturer/index.html'
    context_object_name = 'manufacturers'
    queryset = Manufacturer.objects.all().order_by('name')
    paginate_by = 10

####################################################################################################

@login_required
def details(request, manufacturer_id):

    manufacturer = get_object_or_404(Manufacturer, pk=manufacturer_id)

    return render_to_response('GroupedPurchaseOrder/manufacturer/details.html',
                              {'manufacturer': manufacturer},
                              context_instance=RequestContext(request))

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
