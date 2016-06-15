from __future__ import absolute_import

from django.conf.urls import patterns, url
from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse_lazy


urlpatterns = patterns('accounts.views',
    url(r'^login/$',
        auth_views.login, {'template_name': 'registration/login.html'},
        name='auth_login'),
    url(r'^logout/$',
        auth_views.logout, {'template_name': 'registration/logout.html'},
        name='auth_logout'),
    url(r'^login/modal/$',
        auth_views.login, {'template_name':
        'registration/fragments/login_modal.html'},
        name='auth_login_modal'),
    url(r'^login/error/$', 'login_error', name='login_error'),

    url(r'^password/reset/$',
        auth_views.password_reset,
        {'post_reset_redirect': reverse_lazy('auth_password_reset_done'),
        'html_email_template_name': 'registration/password_reset_email.html'},
        name='auth_password_reset'),
    url(r'^password/reset/done/$',
        auth_views.password_reset_done,
        name='auth_password_reset_done'),
    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        {'post_reset_redirect': reverse_lazy('auth_password_reset_complete')},
        name='password_reset_confirm'),
    url(r'^password/reset/complete/$',
        auth_views.password_reset_complete,
        name='auth_password_reset_complete'),
    url(r'^password/change/$',
        auth_views.password_change,
        {'post_change_redirect': reverse_lazy('auth_password_change_done')},
        name='auth_password_change'),
    url(r'^password/change/done/$',
        auth_views.password_change_done,
        name='auth_password_change_done'),

    url(r'^profile/$', 'profile_page', {'username': None},
        name='profile_page'),
    url(r'^profile/edit/$', 'profile_edit', name='profile_edit'),
    url(r'^profile/(?P<username>[A-Za-z0-9_+-@\.]+)$', 'profile_page',
        name='profile_page_for_user'),
)
