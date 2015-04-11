# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import (
    HomePage,
    MapPageView,

    CropFieldDetailView,
    CropFieldCreateView,
    CropFieldUpdateView,
    CropFieldDeleteView,

    IndividualEntryDetailView,
    CropFieldEntriesListView,
    EntryCreateView,
    EntryUpdateView,
    EntryDeleteView,

    AlertsView,

    MobileLoginView
)


urlpatterns = patterns(
    '',
    url(r'^$', HomePage.as_view(), name='homepage'),

    url(r'^map/$', MapPageView.as_view(), name='map'),

    url(
        r'^crop-field/(?P<pk>\d+)/$',
        CropFieldDetailView.as_view(),
        name='crop-field-detail'
    ),
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
        r'^delete-crop-field/(?P<pk>\d+)/$',
        CropFieldDeleteView.as_view(),
        name="delete_crop_field"
    ),

    url(
        r'^entry/(?P<pk>\d+)/$',
        IndividualEntryDetailView.as_view(),
        name='entry-detail'
    ),
    url(
        r'^crop-field/(?P<pk>\d+)/entries$',
        CropFieldEntriesListView.as_view(),
        name='crop-field-entries'
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
        r'^delete-entry/(?P<pk>\d+)/$',
        EntryDeleteView.as_view(),
        name="delete_entry"
    ),

    url(
        r'^alerts/$',
        AlertsView.as_view(),
        name="alerts-page"
    ),

    url(
        r'^mobile-login/$',
        MobileLoginView.as_view()
    ),
)
