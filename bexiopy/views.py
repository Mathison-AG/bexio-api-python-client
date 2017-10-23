# -*- coding: utf-8 -*-
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import TemplateView

from .api import BexiopyAuth


class HomePage(TemplateView):
    """
    Basic home page.
    """
    template_name = "base_bs4.html"


class BexioAuthentication(TemplateView):
    """
    This is the main view in which we authenticate ourselves with Bexio,
    which is required to use the api.
    """
    def __init__(self, *args, **kwargs):
        super(BexioAuthentication, self).__init__(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        auth_api = BexiopyAuth()

        code = self.request.GET.get('code', None)
        state = self.request.GET.get('state', None)
        print(code, state)
        if (code and state):

            if auth_api.has_authenticated(code, state):
                messages.success(request, "Success")
        
        return redirect('/')

        # elif not auth_api.has_authenticated:
        #     return redirect(auth_api.authenticate())

        # if kwargs.get('code', None):
        #     messages.success(request, auth_api['message'])
        # else:
        #     messages.warning(request, auth_api['message'])


"""
https://office.bexio.com/oauth/authorize?
client_id=9170616879.apps.bexio.com
scope=kb_invoice_edit
client_secret=WbH5Di/6g+Te+cIElwJZI3jYMdo=
redirect_uri=https://www.oesah.de
state=_ae5fd8d6c69d6f72708dbbce723aa9dd38390af373:http://my.bexio.com/simplesaml/saml2/idp/SSOService.php?spentityid=easysys%26amp;cookieTime=1508419466
"""