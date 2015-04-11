# -*- coding: utf-8 -*-
import logging
LOG = logging.getLogger(__name__)

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site

# For Project Prototype purposes.
# TODO: Remove anything related to plain text passwords.
from django.contrib.auth.hashers import BasePasswordHasher

from django.views.generic import (
    TemplateView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    ListView,
    View
)

from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer

from braces.views import (
    JsonRequestResponseMixin,
    CsrfExemptMixin,
    LoginRequiredMixin
)

from django.contrib.auth.models import User

from .models import CropField, Entry, Alert

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


class CropFieldDeleteView(LoginRequiredMixin, DeleteView):
    model = CropField
    success_url = '/map'
    template_name = 'confirm_delete_crop_field.html'

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = self.get_cancel_url()
            return HttpResponseRedirect(url)
        else:
            return super(CropFieldDeleteView, self).post(
                request,
                *args,
                **kwargs)

    def get_cancel_url(self):
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

        self.fire_alerting_process(self.object)

        return super(EntryCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('map')

    def fire_alerting_process(self, entry):
        if entry.crop_field:
            location = entry.crop_field.area.point_on_surface
        else:
            location = entry.location

        # Find all cropfields near the entry (2km)
        crop_fields = CropField.objects.filter(
            area__distance_lte=(location, 2000)
        ).exclude(creator=entry.creator)

        users_to_email = []

        for field in crop_fields:
            if field.creator not in users_to_email:
                users_to_email.append(field.creator)

            alert = Alert(
                entry=entry,
                crop_field=field,
                user=field.creator
            )

            alert.save()

        for user in users_to_email:
            alerts_page_link = (
                'http://' + get_current_site(self.request).domain + '/alerts/'
            )
            self.send_email(user.email, alerts_page_link)

    def send_email(self, email, alerts_page_link):
        send_mail(
            'Notification From Save My Crops',
            (
                'Alert Notification from Save My Crops \n\n' +
                'Pest or Disease was reported near your crop fields. \n' +
                'Visit your Alerts page at Save My Crops to find out more. ' +
                '\n\n Follow this link: ' +
                alerts_page_link +
                '\n\n' +
                'Dedicated to saving your crops, \n' +
                'Save My Crops team.'
            ),
            # FROM_EMAIL
            'alerts@savemycrops.com',
            [email],
            fail_silently=False,
            html_message=(
                '<html><body>' +

                '<h4>Alert Notification from Save My Crops</h4></br></br>' +
                '<p>Pest or Disease was reported near your crop fields.</p>' +
                '<p><a href="' + alerts_page_link + '">' +
                'Visit your Alerts page</a> ' +
                'at <b>Save My Crops<b> to find out more.</p> </br></br>' +
                '<p>Dedicated to saving your crops,</p>' +
                '<p><b>Save My Crops team</b>.</p>'

                '</body></html>'
            )
        )


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


class EntryDeleteView(LoginRequiredMixin, DeleteView):
    model = Entry
    success_url = '/map'
    template_name = 'confirm_delete_entry.html'

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = self.get_cancel_url()
            return HttpResponseRedirect(url)
        else:
            return super(EntryDeleteView, self).post(
                request,
                *args,
                **kwargs)

    def get_cancel_url(self):
        return reverse('map')


class CropFieldDetailView(DetailView):
    model = CropField
    template_name = 'crop_field_detail.html'


class IndividualEntryDetailView(DetailView):
    model = Entry
    template_name = 'entry_detail.html'


class CropFieldEntriesListView(DetailView):
    model = CropField
    template_name = 'crop_field_entries.html'

    def get_context_data(self, **kwargs):
        context = super(CropFieldEntriesListView, self).get_context_data(
            **kwargs)

        context['entries'] = self.object.entries.all()

        return context


class AlertsView(ListView):
    model = Alert
    template_name = 'alerts.html'

    def get_context_data(self, **kwargs):
        context = super(AlertsView, self).get_context_data(**kwargs)

        alerts = Alert.objects.filter(
            user=self.request.user
        ).order_by('creation_time')

        context['alerts'] = alerts

        # for alert in alerts:
        #     alert.is_viewed = True
        #     alert.save()

        return context


class PlainTextPasswordHasher(BasePasswordHasher):
    """
    For Project Prototype purposes.
    TODO: Remove anything related to plain text passwords.
    """
    algorithm = 'plain'

    def salt(self):
        return ''

    def verify(self, password, encoded):
        return self.encode(password) == encoded

    def encode(self, password, salt=None):
        return "%s$1$%s" % (self.algorithm, password)


class MobileLoginView(
    CsrfExemptMixin,
    PlainTextPasswordHasher,
    JsonRequestResponseMixin,
        View):
    http_method_names = [u'get', u'post']
    # require_json = True

    def post(self, request, *args, **kwargs):
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = User.objects.get(username=username)

            # For Project Prototype purposes.
            # TODO: Remove anything related to plain text passwords.
            if self.verify(password, user.password):
                crop_fields_json = JSONRenderer().render(
                    CropFieldSerializer(user.crop_fields, many=True).data
                )
                individual_entries_json = JSONRenderer().render(
                    IndividualEntriesSerializer(user.entries, many=True).data
                )

                response_data = {
                    'userId': user.id,
                    'userName': user.username,
                    'userEmail': user.email,
                    'cropFieldsNum': user.crop_fields__count,
                    'reportNum': user.entries__count,
                    'cropFields': crop_fields_json,
                    'reports': individual_entries_json
                }
                return self.render_json_response(response_data)
            else:
                error_dict = {u"message": (u"Wrong usrename or password")}
                return self.render_bad_request_response(error_dict)
        except:
            error_dict = {u"message": (u"You must submit login creditals")}
            return self.render_bad_request_response(error_dict)
