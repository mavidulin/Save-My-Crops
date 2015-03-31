# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import (
    HomePage,
    MapPageView,
    CropFieldCreateView,
    CropFieldUpdateView,
    EntryCreateView,
    EntryUpdateView,
    CropFieldDetailView,
    IndividualEntryDetailView,
    MyCropFieldsView,
    MyEntriesView
)


urlpatterns = patterns(
    '',
    url(r'^$', HomePage.as_view(), name='homepage'),

    url(r'^map/$', MapPageView.as_view(), name='map'),
    url(
        r'^add-crop-field/$',
        CropFieldCreateView.as_view(),
        name='add-crop-field'
    ),
    url(
        r'^edit-crop-field/(?P<pk>\d+)/$',
        CropFieldUpdateView.as_view(),
        name='edit-crop-field'
    ),
    url(
        r'^add-entry/$',
        EntryCreateView.as_view(),
        name='add-entry'
    ),
    url(
        r'^edit-entry/(?P<pk>\d+)/$',
        EntryUpdateView.as_view(),
        name='edit-entry'
    ),
    url(
        r'^crop-field/(?P<pk>\d+)/$',
        CropFieldDetailView.as_view(),
        name='crop-field-detail'
    ),
    url(
        r'^individual-entry/(?P<pk>\d+)/$',
        IndividualEntryDetailView.as_view(),
        name='entry-detail'
    ),
    url(
        r'^my-crop-fields/$',
        MyCropFieldsView.as_view(),
        name='my-crop-fields'
    ),
    url(r'^my-entries/$', MyEntriesView.as_view(), name='my-entries'),
)
