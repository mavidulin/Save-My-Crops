# -*- coding: utf-8 -*-
import logging
LOG = logging.getLogger(__name__)

from django.views.generic import TemplateView

# from .models import ...


class HomePage(TemplateView):
    template_name = 'homepage.html'


class MapPageView(TemplateView):
    template_name = 'map.html'


class MyCropFieldsView(TemplateView):
    template_name = 'mycrops.html'


class MyEntriesView(TemplateView):
    template_name = 'myentries.html'
