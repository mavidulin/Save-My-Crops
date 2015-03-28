# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import (
    HomePage,
    MapPageView,
    MyCropFieldsView,
    MyEntriesView
)


urlpatterns = patterns(
    '',
    url(r'^$', HomePage.as_view(), name='homepage'),

    url(r'^map/$', MapPageView.as_view(), name='map'),
    url(
        r'^my-crop-fields/$',
        MyCropFieldsView.as_view(),
        name='my-crop-fields'
    ),
    url(r'^my-entries/$', MyEntriesView.as_view(), name='my-entries'),
)
