# -*- coding: utf-8 -*-
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import TemplateView

from .api import Client


class BexioAuthentication(TemplateView):
    """
    This is the main view in which we authenticate ourselves with Bexio,
    which is required to use the api.
    """
    def __init__(self, *args, **kwargs):
        super(BexioAuthentication, self).__init__(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        code = request.GET.get('code')
        client = Client()
        # If code is not set we need to get the authentication code
        print(request.GET)
        if not request.GET.get('code'):
            print("no")
            redirect_to = client.get_oauth2_auth_url()
            return redirect(redirect_to)
        else:
            print("yes")
            client.fetch_access_token_with_auth_code(code)
            messages.info(self.request, 'Successfully connected to Bexio.')
            return redirect('/')
