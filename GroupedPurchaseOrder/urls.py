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

from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView, RedirectView

from notification.views import notice_settings
import django_messages.views as messages_views
from tastypie.api import Api

####################################################################################################

from .api import SupplierResource, OrderResource
# from .views.main import MainView
from .views.account import (AuthenticationForm,
                                                PasswordChangeForm,
                                                PasswordResetForm,
                                                SetPasswordForm)
from .views.angular import CrudOrderView
from .views.manufacturer import (ManufacturerListView, ManufacturerCatalogListView)
from .views.order import (OrderListView)
from .views.supplier import (SupplierListView)
from .views.user_order import (UserOrderListView)

####################################################################################################
#
# Main page
#

# Fixme: name: a.b or a_b ?

urlpatterns = [
    # url(r'^$', MainView.as_view(), name='index'),
    url(r'^$',
        TemplateView.as_view(template_name='GroupedPurchaseOrder/main/index.html'),
        name='index'),
]

####################################################################################################
#
# Authentication
#

import django.contrib.auth.views as auth_views

urlpatterns += [
   url(r'^accounts/login/$',
       auth_views.login,
       {'template_name': 'GroupedPurchaseOrder/account/login.html',
        'authentication_form': AuthenticationForm},
       name='accounts.login'),

    url(r'^accounts/logout/$',
        auth_views.logout,
        {'template_name': 'GroupedPurchaseOrder/account/logged_out.html'},
        name='accounts.logout'),

    url(r'^accounts/password/change/$',
        auth_views.password_change,
        {'template_name': 'GroupedPurchaseOrder/account/password_change.html',
         'password_change_form': PasswordChangeForm,
         'post_change_redirect': reverse_lazy('accounts.password_change_done')},
        name='accounts.password_change'),

    url(r'^accounts/password/reset/$',
        auth_views.password_reset,
        {'template_name': 'GroupedPurchaseOrder/account/password_reset.html',
         'email_template_name': 'GroupedPurchaseOrder/account/password_reset_email.txt',
         'password_reset_form': PasswordResetForm,
         'post_reset_redirect': reverse_lazy('accounts.password_reset_done')},
        name='accounts.password_reset'),

    url(r'^accounts/password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        {'template_name': 'GroupedPurchaseOrder/account/password_reset_confirm.html',
         'set_password_form': SetPasswordForm},
        name='accounts.password_reset_confirm'),

    url(r'^accounts/password/reset/complete/$',
        auth_views.password_reset_complete,
        {'template_name': 'GroupedPurchaseOrder/account/password_reset_complete.html'},
        name='password_reset_complete'),
]

####################################################################################################
#
# Profile
#

import GroupedPurchaseOrder.views.account as account_views

urlpatterns += [
    url(r'^accounts/register/$',
        account_views.register,
        name='accounts.register'),

    url(r'^accounts/register/(?P<user_id>\d+)/confirm/(?P<user_hash>\w+)/$',
        account_views.register_confirm,
        name='accounts.register.confirm'),

    url(r'^accounts/profile/$',
        account_views.profile,
        name='accounts.profile'),

    url(r'^accounts/profile/update/$',
        account_views.update,
        name='accounts.profile.update'),

    url(r'^accounts/password/change/done/$',
        account_views.password_change_done,
        name='accounts.password_change_done'),

    url(r'^accounts/password/reset/done/$',
        account_views.password_reset_done,
        name='accounts.password_reset_done'),

    url(r'^accounts/delete/$',
        account_views.delete,
        name='accounts.delete'),
]

####################################################################################################
#
# Notification
#

urlpatterns += [
    url(r"^settings/$",
        notice_settings,
        # {'template_name': 'GroupedPurchaseOrder/notification/notice_settings.html',},
        name="notification_notice_settings"),
]

####################################################################################################
#
# Messages
#

# url(r'^messages/', include('django_messages.urls')),

urlpatterns += [
    url(r'^messages/$',
        RedirectView.as_view(url='inbox/'),
        name='messages_redirect'),

    url(r'^messages/inbox/$',
        messages_views.inbox,
        {'template_name': 'GroupedPurchaseOrder/messages/inbox.html',},
        name='messages_inbox'),

    url(r'^messages/outbox/$',
        messages_views.outbox,
        {'template_name': 'GroupedPurchaseOrder/messages/outbox.html',},
        name='messages_outbox'),

    url(r'^messages/compose/$',
        messages_views.compose,
        {'template_name': 'GroupedPurchaseOrder/messages/compose.html',},
        name='messages_compose'),

    url(r'^messages/compose/(?P<recipient>[\w.@+-]+)/$',
        messages_views.compose,
        {'template_name': 'GroupedPurchaseOrder/messages/compose.html',},
        name='messages_compose_to'),

    url(r'^reply/(?P<message_id>[\d]+)/$',
        messages_views.reply,
        {'template_name': 'GroupedPurchaseOrder/messages/compose.html',},
        name='messages_reply'),

    url(r'^messages/view/(?P<message_id>[\d]+)/$',
        messages_views.view,
        {'template_name': 'GroupedPurchaseOrder/messages/view.html',},
        name='messages_detail'),

    url(r'^messages/delete/(?P<message_id>[\d]+)/$',
        messages_views.delete,
        name='messages_delete'),

    url(r'^messages/undelete/(?P<message_id>[\d]+)/$',
        messages_views.undelete,
        name='messages_undelete'),

    url(r'^messages/trash/$',
        messages_views.trash,
        {'template_name': 'GroupedPurchaseOrder/messages/trash.html',},
        name='messages_trash'),
]

####################################################################################################
#
# Manufacturer
#

import GroupedPurchaseOrder.views.manufacturer as manufacturer_views

urlpatterns += [
    url(r'^manufacturers/$',
        login_required(ManufacturerListView.as_view()),
        name='manufacturers.index'),

    url(r'^manufacturers/create/$',
        manufacturer_views.create,
        name='manufacturers.create'),

    url(r'^manufacturers/(?P<manufacturer_id>\d+)/$',
        # 'details',
        login_required(ManufacturerCatalogListView.as_view()),
        name='manufacturers.details'),

    url(r'^manufacturers/(?P<manufacturer_id>\d+)/update/$',
        manufacturer_views.update,
        name='manufacturers.update'),

    url(r'^manufacturers/(?P<manufacturer_id>\d+)/delete/$',
        manufacturer_views.delete,
        name='manufacturers.delete'),
]

####################################################################################################
#
# Product
#

import GroupedPurchaseOrder.views.product as product_views

urlpatterns += [
    url(r'^products/(?P<manufacturer_id>\d+)/create/$',
        product_views.create,
        name='products.create'),

    url(r'^products/(?P<product_id>\d+)/$',
        product_views.details,
        name='products.details'),

    url(r'^products/(?P<product_id>\d+)/update/$',
        product_views.update,
        name='products.update'),

    url(r'^products/(?P<product_id>\d+)/delete/$',
        product_views.delete,
        name='products.delete'),
]

####################################################################################################
#
# Supplier
#

import GroupedPurchaseOrder.views.supplier as supplier_views

urlpatterns += [
    url(r'^suppliers/$',
        login_required(SupplierListView.as_view()),
        name='suppliers.index'),

    url(r'^suppliers/create/$',
        supplier_views.create,
        name='suppliers.create'),

    url(r'^suppliers/(?P<supplier_id>\d+)/$',
        supplier_views.details,
        name='suppliers.details'),

    url(r'^suppliers/(?P<supplier_id>\d+)/update/$',
        supplier_views.update,
        name='suppliers.update'),

    url(r'^suppliers/(?P<supplier_id>\d+)/delete/$',
        supplier_views.delete,
        name='suppliers.delete'),

    url(r'^suppliers/(?P<supplier_id>\d+)/catalog/$',
        supplier_views.catalog,
        name='suppliers.catalog'),
]

####################################################################################################
#
# Supplier Product
#

import GroupedPurchaseOrder.views.supplier_product as supplier_product_views

urlpatterns += [
    url(r'^supplier_products/(?P<product_id>\d+)/create/$',
        supplier_product_views.create,
        name='supplier_products.create'),

    url(r'^supplier_products/(?P<supplier_product_id>\d+)/update/$',
        supplier_product_views.update,
        name='supplier_products.update'),

    url(r'^supplier_products/(?P<supplier_product_id>\d+)/delete/$',
        supplier_product_views.delete,
        name='supplier_products.delete'),
]

####################################################################################################
#
# Order
#

import GroupedPurchaseOrder.views.order as order_views

urlpatterns += [
    url(r'^orders/$',
        login_required(OrderListView.as_view()),
        name='orders.index'),

    url(r'^orders/create/$',
        order_views.create,
        name='orders.create'),

    url(r'^orders/(?P<order_id>\d+)/$',
        order_views.details,
        name='orders.details'),

    url(r'^orders/(?P<order_id>\d+)/csv/$',
        order_views.upload_csv,
        name='orders.csv'),

    url(r'^orders/(?P<order_id>\d+)/update/$',
        order_views.update,
        name='orders.update'),

    url(r'^orders/(?P<order_id>\d+)/delete/$',
        order_views.delete,
        name='orders.delete'),
]

####################################################################################################
#
# User Order
#

import GroupedPurchaseOrder.views.user_order as user_order_views

urlpatterns += [
    url(r'^user_orders/$',
        login_required(UserOrderListView.as_view()),
        name='user_orders.index'),

    # url(r'^user_orders/(?P<user_order_id>\d+)/$',
    #     user_order_views.details,
    #     name='user_orders.details'),

    url(r'^user_orders/(?P<user_order_id>\d+)/update/$',
        user_order_views.update,
        name='user_orders.update'),

    # url(r'^user_orders/(?P<user_order_id>\d+)/delete/$',
    #     user_order_views.delete,
    #     name='user_orders.delete'),
]

####################################################################################################
#
# Product Order
#

import GroupedPurchaseOrder.views.product_order as product_order_views

urlpatterns += [
    url(r'^product_orders/create/(?P<supplier_product_id>\d+)/$',
        product_order_views.create,
        name='product_orders.create'),

    url(r'^product_orders/create_xhr/(?P<supplier_product_id>\d+)/$',
        product_order_views.create_xhr,
        name='product_orders.create_xhr'),

    url(r'^product_orders/(?P<product_order_id>\d+)/$',
        product_order_views.details,
        name='product_orders.details'),

    url(r'^product_orders/(?P<product_order_id>\d+)/update/$',
        product_order_views.update,
        name='product_orders.update'),

    url(r'^product_orders/(?P<product_order_id>\d+)/update_xhr/$',
        product_order_views.update_xhr,
        name='product_orders.update_xhr'),

    url(r'^product_orders/(?P<product_order_id>\d+)/delete/$',
        product_order_views.delete,
        name='product_orders.delete'),
]

####################################################################################################

# django-angular test

urlpatterns += [
  # http://127.0.0.1:8000/crud/orders/
  # http://127.0.0.1:8000/crud/orders/?pk=1
  url(r'^crud/orders/?$', CrudOrderView.as_view(), name='crud_orders_view'),

  url(r'^angular_test/$',
      TemplateView.as_view(template_name='GroupedPurchaseOrder/angular_test/page.html'),
      name='angular_test'),
]

####################################################################################################

# Tastypie test

v1_api = Api(api_name='v1')
v1_api.register(SupplierResource())
v1_api.register(OrderResource())

urlpatterns += [
    # http://127.0.0.1:8000/api/v1/order/?format=json
    # http://127.0.0.1:8000/api/v1/order/1/?format=json
    url(r'^api/', include(v1_api.urls)),
]

####################################################################################################

# Ajax test
# urlpatterns += patterns('GroupedPurchaseOrder.views.ajax',
#     url(r'^ajax/hello$',
#         'hello',
#         name='ajax.hello'),
#
#     url(r'^ajax/bye$',
#         'bye',
#         name='ajax.bye'),
# )

####################################################################################################
#
# End
#
####################################################################################################
