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

from tastypie import fields
from tastypie.authentication import SessionAuthentication, ApiKeyAuthentication
from tastypie.resources import ModelResource
from tastypie.authorization import DjangoAuthorization, ReadOnlyAuthorization

####################################################################################################

from .models import Supplier, Order

####################################################################################################

class SupplierResource(ModelResource):

    class Meta:
        queryset = Supplier.objects.all()
        resource_name = 'supplier'
        # authentication = ApiKeyAuthentication()
        authentication = SessionAuthentication()
        authorization = ReadOnlyAuthorization()

####################################################################################################

class OrderResource(ModelResource):

    # supplier = fields.ForeignKey(SupplierResource, 'supplier')

    class Meta:
        queryset = Order.objects.all()
        resource_name = 'order'
        # authentication = ApiKeyAuthentication()
        authentication = SessionAuthentication()
        authorization = ReadOnlyAuthorization()

    ##############################################

    def dehydrate(self, bundle):

        bundle.data['name'] = bundle.obj.name()
        bundle.data['supplier'] = bundle.obj.supplier.pk
        return bundle

####################################################################################################
# 
# End
# 
####################################################################################################
