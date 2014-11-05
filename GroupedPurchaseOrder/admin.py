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

from django.contrib import admin
from GroupedPurchaseOrder.models import (Profile,
                                         Supplier,
                                         Manufacturer,
                                         Product,
                                         SupplierProduct,
                                         Order,
                                         UserOrder,
                                         ProductOrder)

####################################################################################################

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'language', 'timezone')

####################################################################################################

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # list_display = ('name')
    list_filter = ['manufacturer']
    search_fields = ['part_number', 'name', 'description']

####################################################################################################

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'status')
    list_filter = ['status']
    search_fields = ['name']

####################################################################################################

# class OrderInline(admin.TabularInline):
#     model = Order
#     fields = ('status',)

####################################################################################################

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    pass
    # inlines = [
    #     OrderInline,
    # ]

####################################################################################################

#admin.site.register(Order)
#admin.site.register(Product)
#admin.site.register(Profile)
admin.site.register(Manufacturer)
admin.site.register(ProductOrder)
#admin.site.register(Supplier)
admin.site.register(SupplierProduct)
admin.site.register(UserOrder)

####################################################################################################
# 
# End
# 
####################################################################################################
