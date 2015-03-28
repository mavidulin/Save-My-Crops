# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib.auth.views import (
    password_reset,
    password_reset_done,
    password_reset_confirm,
    password_reset_complete,
    password_change,
    password_change_done
)

from .views import UserProfileView, AccountDeleteView


urlpatterns = patterns(
    '',
    url(
        r'^profile/$',
        UserProfileView.as_view(),
        name="userprofilepage"
    ),
    url(
        r'^delete/(?P<pk>\d+)/$',
        AccountDeleteView.as_view(),
        name="account_delete"
    ),

    url(r'^logout/$',
        'django.contrib.auth.views.logout',
        {'next_page': '/'}, name='custom_logout'),

    url(
        r'^password/reset/$',
        password_reset,
        {
            'template_name': 'custom-registration/password_reset_form.html',
            'email_template_name': 'custom-registration/password_reset_email.html'
        },
        name="password_reset"
    ),
    url(
        r'^password/reset/done/$',
        password_reset_done,
        {'template_name': 'custom-registration/password_reset_done.html'},
        name='password_reset_done'
    ),
    url(
        r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        password_reset_confirm,
        {'template_name': 'custom-registration/password_reset_confirm.html'},
        name='password_reset_confirm'
    ),
    url(
        r'^password/reset/complete/$',
        password_reset_complete,
        {'template_name': 'custom-registration/password_reset_complete.html'},
        name='password_reset_complete'
    ),

    url(
        r'^password/change/$',
        password_change,
        {'template_name': 'custom-registration/password_change_form.html'},
        name='password_change'
    ),
    url(
        r'^password/change/done/$',
        password_change_done,
        {'template_name': 'custom-registration/password_change_done.html'},
        name='password_change_done'
    ),
)
