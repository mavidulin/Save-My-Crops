# -*- coding: utf-8 -*-
import logging
LOG = logging.getLogger(__name__)

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User

from django.views.generic import TemplateView, DeleteView

from braces.views import LoginRequiredMixin

# from .models import ...


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'userprofile.html'


class AccountDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = '/'
    template_name = 'confirm_delete_account.html'

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = self.get_cancel_url()
            return HttpResponseRedirect(url)
        else:
            return super(AccountDeleteView, self).post(
                request,
                *args,
                **kwargs)

    def get_cancel_url(self):
        return reverse('userprofilepage')
