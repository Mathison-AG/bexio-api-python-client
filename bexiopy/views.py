# -*- coding: utf-8 -*-
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import TemplateView

from .api import BexiopyAuth, Bexiopy


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
        if code:
            response = auth_api.get_api_access_token(code)
            if response.status_code == 200:
                messages.success(request, "Success")
            else:
                messages.error(request, "Error")
            return redirect('/')
        else:
            return redirect(BexiopyAuth.get_authentication_url())


        # elif not auth_api.has_authenticated:
        #     return redirect(auth_api.authenticate())

        # if kwargs.get('code', None):
        #     messages.success(request, auth_api['message'])
        # else:
        #     messages.warning(request, auth_api['message'])

