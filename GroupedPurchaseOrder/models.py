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

import binascii
import os
import pytz

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext as _

####################################################################################################

from .settings import LANGUAGES

####################################################################################################

def random_hash():
    """ Create a random string of size 30 """
    return binascii.b2a_hex(os.urandom(15))

####################################################################################################

def all_timezones():
    return [(tz, tz) for tz in pytz.all_timezones]

####################################################################################################

class CurrencyField(models.DecimalField):
    def __init__(self, **options):
        decimal_places = options.setdefault('decimal_places', 5)
        options.setdefault('max_digits', 10 + decimal_places) # billion
        super(CurrencyField, self).__init__(**options)

####################################################################################################

class Profile(models.Model):

    class Meta:
        app_label = 'GroupedPurchaseOrder'

    # http:// /doc/ref/contrib/auth.html#django.contrib.auth.models.User
    user = models.OneToOneField(User)
    phone_number = models.CharField(max_length=30, blank=True, null=True)
    # hash_id is used to confirm the profile
    hash_id = models.CharField(unique=True, max_length=30, default=random_hash)
    language = models.CharField(max_length=4, blank=True, null=True, choices=LANGUAGES)
    timezone = models.CharField(max_length=40, choices=all_timezones(), default='UTC')

    ##############################################

    def clean(self):

        if self.timezone == 'UTC':
            # Fixme: dict?
            raise ValidationError({'timezone': [_('UTC is not valid timezone')]})

    ##############################################

    def __str__(self):
        return "{}".format(self.user)

####################################################################################################

class Supplier(models.Model):

    class Meta:
        app_label = 'GroupedPurchaseOrder'

    creation_date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, unique=True)
    url = models.URLField(null=True, blank=True)
    purchase_therms_url = models.URLField(null=True, blank=True, verbose_name='Therms of purchase')
    delivery_therms_url = models.URLField(null=True, blank=True, verbose_name='Therms of delivery') # shipping_conditions
    description = models.TextField(default='', blank=True)
    minimum_purchase = CurrencyField(default=0) # HT ?
    free_shipment_threshold = CurrencyField(default=0) # HT ?
    # currency = models.CharField(max_length=3, default='€')

    ##############################################

    def __str__(self):
        return "{}".format(self.name)

####################################################################################################

class Manufacturer(models.Model):

    class Meta:
        app_label = 'GroupedPurchaseOrder'

    creation_date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100, unique=True)
    url = models.URLField(null=True, blank=True)

    ##############################################

    def __str__(self):
        return "{}".format(self.name)

####################################################################################################

class Product(models.Model):

    class Meta:
        app_label = 'GroupedPurchaseOrder'

    creation_date = models.DateTimeField(auto_now_add=True)
    manufacturer = models.ForeignKey(Manufacturer)
    part_number = models.CharField(max_length=100, default='', blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField(default='', blank=True)
    url = models.URLField(null=True, blank=True)
    # category: electronic/resistor/.../...

    ##############################################

    def __str__(self):
        return self.full_name()

    ##############################################

    def full_name(self):
        return "{} - {}".format(self.manufacturer.name, self.name)

    ##############################################

    def manufacturer_name(self):
        return self.manufacturer.name

####################################################################################################

class SupplierProduct(models.Model):

    class Meta:
        app_label = 'GroupedPurchaseOrder'

    creation_date = models.DateTimeField(auto_now_add=True)
    supplier = models.ForeignKey(Supplier)
    product = models.ForeignKey(Product)
    order_code = models.CharField(max_length=100)
    price = CurrencyField(default=0) # HT ?
    url = models.URLField(null=True, blank=True)

    ##############################################

    def __str__(self):
        return self.name()

    ##############################################

    def name(self):
        return "{} - {}".format(self.supplier.name, self.order_code)

####################################################################################################

class Order(models.Model):

    ORDER_STATUS = (
        ('new', 'new'),
        ('ordered', 'ordered'),
        ('delivered', 'delivered'),
    )

    class Meta:
        app_label = 'GroupedPurchaseOrder'

    creation_date = models.DateTimeField(auto_now_add=True)
    supplier = models.ForeignKey(Supplier)
    order_date = models.DateTimeField(null=True, blank=True)
    delivery_date = models.DateTimeField(null=True, blank=True)
    manager = models.ForeignKey(Profile, null=True, blank=True)
    status = models.CharField(max_length=len('delivered'), choices=ORDER_STATUS, default='new')
    total = CurrencyField(default=0, help_text='Please fill the total excluding taxes') # HT ?
    duty_tax = CurrencyField(default=0, help_text='Please fill any duty tax') # HT ?
    shipping_rate = CurrencyField(default=0, help_text='Please fill the amount ex VAT') # HT ?
    vat_tax = CurrencyField(default=0) # HT ?

    # duty_tax
    # shipping_rate
    # total/sum (+ duty_tax + shipping_rate)

    ##############################################

    def __str__(self):
        return self.name()

    ##############################################

    def name(self):
        return "{} - {}".format(self.supplier.name, self.pk)

####################################################################################################

class UserOrder(models.Model):

    ORDER_STATUS = (
        ('new', 'new'),
        ('cancelled', 'cancelled'),
        ('ordered', 'ordered'),
        ('delivered', 'delivered'),
    )

    class Meta:
        app_label = 'GroupedPurchaseOrder'

    creation_date = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey(Order)
    profile = models.ForeignKey(Profile)
    status = models.CharField(max_length=len('delivered'), choices=ORDER_STATUS, default='new')
    payed = models.BooleanField(default=False)
    delivery_date = models.DateTimeField(null=True, blank=True)
    # duty_tax
    # shipping_rate
    # total/sum (+ duty_tax + shipping_rate)

    ##############################################

    def __str__(self):
        return self.name()

    ##############################################

    def name(self):
        return "{} - {}".format(str(self.order), str(self.profile))

####################################################################################################

class ProductOrder(models.Model):

    class Meta:
        app_label = 'GroupedPurchaseOrder'

    creation_date = models.DateTimeField(auto_now_add=True)
    user_order = models.ForeignKey(UserOrder)
    supplier_product = models.ForeignKey(SupplierProduct) # must be limited to supplier
    quantity = models.PositiveIntegerField(default=1)
    # (cf. odoo remise, unit price spécifique ...)

    ##############################################

    def __str__(self):
        return self.name()

    ##############################################

    def name(self):
        return "{} - {}".format(str(self.user_order), self.pk)

####################################################################################################
# 
# End
# 
####################################################################################################
