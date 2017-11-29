# -*- coding: utf-8 -*-
from django.views.generic import TemplateView

from bexiopy.api import Bexiopy


class HomePage(TemplateView):
    """
    Basic home page.
    """
    template_name = "base_bs4.html"

    def get_context_data(self, **kwargs):
        context = super(HomePage, self).get_context_data(**kwargs)
        bexio = Bexiopy()
        context['invoices'] = bexio.invoices.all()
        context['contacts'] = bexio.contacts.all()
        context['salutations'] = bexio.general.get_salutations()
        context['titles'] = bexio.general.get_titles()

        # data = {
        #     'contact_type_id': 1,
        #     'name_1': 'Özer Sahin 22',
        #     'owner_id': 1,
        #     'user_id': 1
        # }
        # context['contacts'] = "Test: %s" % Bexiopy.contacts.update_or_create(
        #     oid=7, **data)
        return context
