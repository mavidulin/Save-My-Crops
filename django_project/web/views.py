# -*- coding: utf-8 -*-
import logging
LOG = logging.getLogger(__name__)

from django.core.urlresolvers import reverse
from django.views.generic import (
    TemplateView,
    DetailView,
    CreateView,
    UpdateView
)

from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer

from .models import CropField, Entry

from .forms import CropFieldForm, EntryForm

from .serializers import (
    CropFieldSerializer,
    IndividualEntriesSerializer
)


class HomePage(TemplateView):
    template_name = 'homepage.html'


class CropFieldViewSet(viewsets.ModelViewSet):
    model = CropField
    serializer_class = CropFieldSerializer


class SendFeaturesToContext(object):

    def get_context_data(self, **kwargs):
        context = super(SendFeaturesToContext, self).get_context_data(**kwargs)

        crop_fields = CropField.objects.all()
        individual_entries = Entry.objects.exclude(crop_field__isnull=False)

        context['crop_fields'] = JSONRenderer().render(
            CropFieldSerializer(crop_fields, many=True).data
        )

        context['individual_entries'] = JSONRenderer().render(
            IndividualEntriesSerializer(individual_entries, many=True).data
        )

        return context


class MapPageView(SendFeaturesToContext, TemplateView):
    template_name = 'map.html'


class CropFieldCreateView(SendFeaturesToContext, CreateView):
    model = CropField
    form_class = CropFieldForm
    template_name = 'crop_field_form.html'

    def get_context_data(self, **kwargs):
        context = super(CropFieldCreateView, self).get_context_data(**kwargs)
        context['mode'] = 'create'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.creator = self.request.user
        self.object.save()

        return super(CropFieldCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('map')


class CropFieldUpdateView(SendFeaturesToContext, UpdateView):
    model = CropField
    form_class = CropFieldForm
    template_name = 'crop_field_form.html'

    def get_context_data(self, **kwargs):
        context = super(CropFieldUpdateView, self).get_context_data(**kwargs)
        context['mode'] = 'update'
        context['editing_geom_id'] = self.kwargs.get('pk')

        return context

    def get_success_url(self):
        return reverse('map')


class EntryFormViewMixin(object):

    def get_form(self, form_class):
        """
        Returns an instance of the form to be used in this view.
        """
        kwargs = self.get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return form_class(**kwargs)


class EntryCreateView(SendFeaturesToContext, EntryFormViewMixin, CreateView):
    model = Entry
    form_class = EntryForm
    template_name = 'entry_form.html'

    def get_context_data(self, **kwargs):
        context = super(EntryCreateView, self).get_context_data(**kwargs)
        context['mode'] = 'create'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.creator = self.request.user

        if self.object.crop_field is None:
            if self.object.location is None:
                form.add_error(
                    None,
                    'Select a Crop Field or place a marker on the map'
                )
                return self.form_invalid(form)

        self.object.save()

        return super(EntryCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('map')


class EntryUpdateView(SendFeaturesToContext, EntryFormViewMixin, UpdateView):
    model = Entry
    form_class = EntryForm
    template_name = 'entry_form.html'

    def get_context_data(self, **kwargs):
        context = super(EntryUpdateView, self).get_context_data(**kwargs)
        context['mode'] = 'update'

        if (self.object.crop_field is None):
            context['editing_geom_id'] = self.kwargs.get('pk')

        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)

        if self.object.crop_field is None:
            if self.object.location is None:
                form.add_error(
                    None,
                    'Select a Crop Field or place a marker on the map'
                )
                return self.form_invalid(form)

        self.object.save()

        return super(EntryUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('map')


class CropFieldDetailView(DetailView):
    model = CropField
    template_name = 'crop_field_detail.html'


class IndividualEntryDetailView(DetailView):
    model = CropField
    template_name = 'crop_field_detail.html'


class MyCropFieldsView(TemplateView):
    template_name = 'mycrops.html'


class MyEntriesView(TemplateView):
    template_name = 'myentries.html'
