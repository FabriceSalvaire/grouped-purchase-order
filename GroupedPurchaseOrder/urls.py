####################################################################################################

from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy

####################################################################################################

# from GroupedPurchaseOrder import views
from GroupedPurchaseOrder.views.account import (AuthenticationForm,
                                                PasswordChangeForm,
                                                PasswordResetForm,
                                                SetPasswordForm)

####################################################################################################

# Fixme: name: a.b or a_b ?

# Main page
urlpatterns = patterns('GroupedPurchaseOrder.views.main',
                       url(r'^$', 'index', name='index'),
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

####################################################################################################
# 
# End
# 
####################################################################################################
