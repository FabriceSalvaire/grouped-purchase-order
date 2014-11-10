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

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView

####################################################################################################

# from GroupedPurchaseOrder.views.main import MainView
from GroupedPurchaseOrder.views.account import (AuthenticationForm,
                                                PasswordChangeForm,
                                                PasswordResetForm,
                                                SetPasswordForm)

from GroupedPurchaseOrder.views.supplier import (SupplierListView)
from GroupedPurchaseOrder.views.order import (OrderListView)

####################################################################################################

# Fixme: name: a.b or a_b ?

# Main page
urlpatterns = patterns('',
   # url(r'^$', MainView.as_view(), name='index'),
    url(r'^$',
        TemplateView.as_view(template_name='GroupedPurchaseOrder/main/index.html'),
        name='index'),
)

# Authentication
urlpatterns += patterns('django.contrib.auth.views',
   url(r'^accounts/login/$',
       'login',
       {'template_name': 'GroupedPurchaseOrder/account/login.html',
        'authentication_form': AuthenticationForm},
       name='accounts.login'),

    url(r'^accounts/logout/$',
        'logout',
        {'template_name': 'GroupedPurchaseOrder/account/logged_out.html'},
        name='accounts.logout'),

    url(r'^accounts/password/change/$',
        'password_change',
        {'template_name': 'GroupedPurchaseOrder/account/password_change.html',
         'password_change_form': PasswordChangeForm,
         'post_change_redirect': reverse_lazy('accounts.password_change_done')},
        name='accounts.password_change'),

    url(r'^accounts/password/reset/$',
        'password_reset',
        {'template_name': 'GroupedPurchaseOrder/account/password_reset.html',
         'email_template_name': 'GroupedPurchaseOrder/account/password_reset_email.txt',
         'password_reset_form': PasswordResetForm,
         'post_reset_redirect': reverse_lazy('accounts.password_reset_done')},
        name='accounts.password_reset'),

    url(r'^accounts/password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        'password_reset_confirm',
        {'template_name': 'GroupedPurchaseOrder/account/password_reset_confirm.html',
         'set_password_form': SetPasswordForm},
        name='accounts.password_reset_confirm'),

    url(r'^accounts/password/reset/complete/$',
        'password_reset_complete',
        {'template_name': 'GroupedPurchaseOrder/account/password_reset_complete.html'},
        name='password_reset_complete'),
)

urlpatterns += patterns('GroupedPurchaseOrder.views.account',
    url(r'^accounts/register/$',
        'register',
        name='accounts.register'),

    url(r'^accounts/register/(?P<user_id>\d+)/confirm/(?P<user_hash>\w+)/$',
        'register_confirm',
        name='accounts.register.confirm'),

    url(r'^accounts/profile/$',
        'profile',
        name='accounts.profile'),

    url(r'^accounts/profile/update/$',
        'update',
        name='accounts.profile.update'),

    url(r'^accounts/password/change/done/$',
        'password_change_done',
        name='accounts.password_change_done'),

    url(r'^accounts/password/reset/done/$',
        'password_reset_done',
        name='accounts.password_reset_done'),

    url(r'^accounts/delete/$',
        'delete',
        name='accounts.delete'),
)

# Supplier
urlpatterns += patterns('GroupedPurchaseOrder.views.supplier',
    url(r'^suppliers/$',
        login_required(SupplierListView.as_view()),
        name='suppliers.index'),

    url(r'^suppliers/create/$',
        'create',
        name='suppliers.create'),

    url(r'^suppliers/(?P<supplier_id>\d+)/$',
        'details',
        name='suppliers.details'),

    url(r'^suppliers/(?P<supplier_id>\d+)/update/$',
        'update',
        name='suppliers.update'),

    url(r'^suppliers/(?P<supplier_id>\d+)/delete/$',
        'delete',
        name='suppliers.delete'),
)

# Order
urlpatterns += patterns('GroupedPurchaseOrder.views.order',
    url(r'^orders/$',
        login_required(OrderListView.as_view()),
        name='orders.index'),

    url(r'^orders/create/$',
        'create',
        name='orders.create'),

    url(r'^orders/(?P<order_id>\d+)/$',
        'details',
        name='orders.details'),

    url(r'^orders/(?P<order_id>\d+)/update/$',
        'update',
        name='orders.update'),

    url(r'^orders/(?P<order_id>\d+)/delete/$',
        'delete',
        name='orders.delete'),
)

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
