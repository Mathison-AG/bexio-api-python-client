# -*- coding: utf-8 -*-
try:
    from django.contrib import messages
    from django.shortcuts import redirect
    from django.views.generic import TemplateView
except ImportError:
    class TemplateView(object):
        pass

from .api import Client


class DjangoBexioAuthentication(TemplateView):
    """
    This view is designed for Django which assists the developer in
    authenticating the Django instance with Bexio, which is required
    to use the api.
    """
    def get(self, request, *args, **kwargs):
        """
        Check the request for paramter :code:`code` and authenticate, if
        it exists and redirect to index page. Otherwise redirect to Bexio
        with the right parameters to authenticate your instance.

        Todo:
            * Add csrf token to authentication process
        """
        code = request.GET.get('code', None)
        client = Client()
        # If code is not set we need to get the authentication code
        if not code:
            redirect_to = client.get_oauth2_auth_url()
        else:
            client.fetch_access_token_with_auth_code(code)
            messages.info(self.request, 'Successfully connected to Bexio.')
            redirect_to = '/'
        return redirect(redirect_to)
