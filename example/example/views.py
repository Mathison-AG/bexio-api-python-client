# -*- coding: utf-8 -*-
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import TemplateView

from bexiopy.api import Bexiopy


class HomePage(TemplateView):
    """
    Basic home page.
    """
    template_name = "base_bs4.html"

    def get_context_data(self, **kwargs):
        context = super(HomePage, self).get_context_data(**kwargs)
        context['invoices'] = "Invoice: %s" % Bexiopy.invoices.get(oid=7)
        context['contacts'] = "Contact: %s" % Bexiopy.contacts.get(oid=1)

        # data = {
        #     'contact_type_id': 1,
        #     'name_1': 'Özer Sahin 22',
        #     'owner_id': 1,
        #     'user_id': 1
        # }
        # context['contacts'] = "Test: %s" % Bexiopy.contacts.update_or_create(
        #     oid=7, **data)
        return context
