# -*- coding: utf-8 -*-
from __future__ import absolute_import

try:
    # For Python 3.0 and later
    from urllib.parse import urlencode
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib import urlencode

import datetime
import os
import requests
import shelve
import uuid

from .settings import get_setting
from .resources import contacts, general, invoices


class OAuth2(object):
    """
    This class handles most of the authentication processes. You need to
    instantiate it, authenticate properly and everything else should be
    automatic.

    To see how to instantiate this class properly, take a look at
    :func:`~bexiopy.api.Client.get_oauth2_service`.

    If you want to create an :code:`access_token` with a :code:`code`,
    you can take a look at
    :func:`~bexiopy.api.Client.fetch_access_token_with_auth_code`.
    """
    def __init__(self, *args, **kwargs):
        self.grant_type = ''
        self.config = {
            'client_id':
                kwargs.get('client_id', ''),

            'client_secret':
                kwargs.get('client_secret', ''),

            'authorization_uri':
                kwargs.get('authorization_uri', ''),

            'refresh_token_credential_uri':
                kwargs.get('refresh_token_credential_uri', ''),

            'token_credential_uri':
                kwargs.get('token_credential_uri', ''),

            'redirect_uri':
                kwargs.get('redirect_uri', ''),

            'issuer':
                kwargs.get('issuer', ''),

            'code':
                kwargs.get('code', ''),

            'refresh_token':
                kwargs.get('refresh_token', ''),

            'username':
                kwargs.get('username', ''),

            'password':
                kwargs.get('password', ''),
        }
        self.set_grant_type(self.get_grant_type())

    def set_refresh_token(self, refresh_token):
        """
        Set :code:`refresh_token` in config and return :code:`None`.

        Args:
            refresh_token (str): the refreh_token from our token

        Returns:
            None: nothing to return
        """
        self.config['refresh_token'] = refresh_token

    def get_refresh_token(self):
        """
        Get and return :code:`refresh_token` from config.

        Returns:
            str: :code:`refresh_token`
        """
        return self.config['refresh_token']

    def get_client_id(self):
        """
        Get and return :code:`client_id` from config.

        Returns:
            str: :code:`client_id`
        """
        return self.config['client_id']

    def set_client_id(self, client_id):
        """
        Set :code:`client_id` in config and return :code:`None`.

        Args:
            client_id (str): the client_id from our token

        Returns:
            None: nothing to return
        """
        self.config['client_id'] = client_id

    def get_client_secret(self):
        """
        Get and return :code:`client_secret` from config.

        Returns:
            str: :code:`client_secret`
        """
        return self.config['client_secret']

    def set_client_secret(self, client_secret):
        """
        Set :code:`client_secret` in config and return :code:`None`.

        Args:
            client_secret (str): the client_secret from our token

        Returns:
            None: nothing to return
        """
        self.config['client_secret'] = client_secret

    def get_code(self):
        """
        Get and return :code:`code` from config.

        Returns:
            str: :code:`code`
        """
        return self.config['code']

    def set_code(self, code):
        """
        Set :code:`code` in config and return :code:`None`.

        Args:
            code (str): the code from our token

        Returns:
            None: nothing to return
        """
        self.config['code'] = code

    def get_redirect_uri(self):
        """
        Get and return :code:`redirect_uri` from config.

        Returns:
            str: :code:`redirect_uri`
        """
        return self.config['redirect_uri']

    def set_redirect_uri(self, redirect_uri):
        """
        Set :code:`redirect_uri` in config and return :code:`None`.

        Args:
            redirect_uri (str): the redirect_uri from our token

        Returns:
            None: nothing to return
        """
        self.config['redirect_uri'] = redirect_uri

    def get_grant_type(self):
        """
        Get and return :code:`grant_type` from config.

        If we want to refresh the token, we need to set :code:`grant_type`
        accordingly:

        .. code-block:: python

            auth = OAuth2().get_oauth2_service()

            # refresh token
            auth.set_grant_type('refresh_token')  # important!
            auth.set_refresh_token(refresh_token)

            credentials = auth.fetch_auth_token()

            # ToDO(oesah): more examples for all grant_types
            ...

        Returns:
            str: :code:`grant_type` or empty string
        """
        if self.grant_type:
            return self.grant_type

        if not self.config['code']:
            return 'authorization_code'

        elif not self.config['refresh_token']:
            return 'refresh_token'

        elif ((not self.config['username']) and (not self.config['password'])):
            return 'password'

        else:
            return ''

    def set_grant_type(self, grant_type):
        """
        Set :code:`grant_type` in config and return :code:`None`.

        Args:
            grant_type (str): the grant_type from our token

        Returns:
            None: nothing to return
        """
        self.grant_type = grant_type

    def fetch_auth_token(self):
        """
        Call method that fetches the token and return
        :code:`access_token`.

        Returns:
            dict: result of :func:`~bexiopy.api.OAuth2.generate_credentials_request`
        """
        return self.generate_credentials_request()

    def generate_credentials_request(self):
        """
        Create the correct URL to authenticate or refresh an existing
        token.

        Returns:
            dict: :code:`access_token` that is created from our request
        """
        uri = self.get_token_credential_uri()
        grant_type = self.get_grant_type()
        params = {
            'grant_type': grant_type
        }

        if grant_type == 'authorization_code':
            params['code'] = self.get_code()
            params['redirect_uri'] = self.get_redirect_uri()
            self.add_client_credentials(params)

        elif grant_type == 'refresh_token':
            uri = self.get_refresh_token_credential_uri()
            params['refresh_token'] = self.get_refresh_token()
            self.add_client_credentials(params)

        headers = {
            'Cache-Control': 'no-store',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.post(uri, data=params, headers=headers)
        return response.json()

    def get_token_credential_uri(self):
        """
        Get and return :code:`token_credential_uri` from config.

        Returns:
            str: :code:`token_credential_uri`
        """
        return self.config['token_credential_uri']

    def get_refresh_token_credential_uri(self):
        """
        Get and return :code:`refresh_token_credential_uri` from config.

        Returns:
            str: :code:`refresh_token_credential_uri`
        """
        return self.config['refresh_token_credential_uri']

    def add_client_credentials(self, params):
        """
        Get, append and return :code:`client_id` and :code:`client_secret`
        to params for requests to Bexio API.

        Args:
            params (dict): dictionary of parameters that is used for requests

        Returns:
            dict: modified :code:`params`
        """
        params['client_id'] = self.get_client_id()
        params['client_secret'] = self.get_client_secret()

        return params


class Client(object):
    """
    The client that is used to communicate with Bexio over the API. Once
    authentication has happened, the client will take over most of the
    work.

    Use the client to perform actions like refreshing the token, making
    a call to the API, get the authentication URL that is needed to create
    an access token, etc.

    Usage:

    .. code-block:: python

        >>> from bexiopy.api import Client

        >>> client = Client()
        >>> client.get_oauth2_auth_url()
        Out: https://office.bexio.com/oauth/authorize?client_secret=....

        >>> client.refresh_token()
        Out: {'access_token': '...', ...}

        >>> client.call('GET', 'salutation')
        Out: [{'id': 1, name': 'Herr'}, {'id': 2, name': 'Frau'}, ...]

    """
    def __init__(self, *args, **kwargs):
        # construct auth data
        self.API_URL = get_setting('BEXIO_API_URL')
        self.OAUTH2_AUTH_URL = get_setting('BEXIO_AUTH_URL')
        self.OAUTH2_TOKEN_URI = get_setting('BEXIO_TOKEN_URL')
        self.OAUTH2_REFRESH_TOKEN_URI = get_setting('BEXIO_TOKEN_REFRESH_URL')

        # construct client data
        self.auth = None
        self.config = {
            'client_id': get_setting('BEXIO_CLIENT_ID'),
            'client_secret': get_setting('BEXIO_CLIENT_SECRET'),
            'redirect_uri': get_setting('BEXIO_APPLICATION_REDIRECTION_URL'),
            'scope': get_setting('BEXIO_APPLICATION_SCOPES'),
            'state': uuid.uuid4()
        }
        # get access_token data from file, if exists
        self.load_access_token_from_file()

    def set_client_id(self, client_id):
        """
        Set :code:`client_id` in config and return :code:`None`.

        Args:
            client_id (str): the client_id from our token

        Returns:
            None: nothing to return
        """
        self.config['client_id'] = client_id

    def get_client_id(self):
        """
        Get and return :code:`client_id` from config.

        Returns:
            str: :code:`client_id`
        """
        return self.config['client_id']

    def set_client_secret(self, client_secret):
        """
        Set :code:`client_secret` in config and return :code:`None`.

        Args:
            client_secret (str): the client_secret from our token

        Returns:
            None: nothing to return
        """
        self.config['client_secret'] = client_secret

    def get_client_secret(self):
        """
        Get and return :code:`client_secret` from config.

        Returns:
            str: :code:`client_secret`
        """
        return self.config['client_secret']

    def set_redirect_uri(self, redirect_uri):
        """
        Set :code:`redirect_uri` in config and return :code:`None`.

        Args:
            redirect_uri (str): the redirect_uri from our token

        Returns:
            None: nothing to return
        """
        self.config['redirect_uri'] = redirect_uri

    def get_redirect_uri(self):
        """
        Get and return :code:`redirect_uri` from config.

        Returns:
            str: :code:`redirect_uri`
        """
        return self.config['redirect_uri']

    def get_org(self):
        """
        Get and return :code:`org` from config.

        Returns:
            str: :code:`org`
        """
        return self.access_token['org']

    def file_put_contents(self, access_token):
        """
        Write response data into a shelve file, which is basically a locally
        stored dictionary.

        Args:
            access_token (dict): access token dict we receive from bexio

        Returns:
            None: nothing to return
        """
        d = shelve.open(get_setting('BEXIO_CREDENTIALS_FILENAME'))

        # write json to file
        for k, v in access_token.items():
            d[k] = v

        # closing is important!
        d.close()

    def set_access_token(self, access_token):
        """
        Set :code:`client_secret` in config and return :code:`None`.

        Args:
            client_secret (str): the client_secret from our token

        Returns:
            None: nothing to return

        Raises:
            ValueError: if :code:`access_token` is not valid dict or
                missing data
        """
        if not isinstance(access_token, dict):
            raise ValueError('Invalid token format: Need dict instead of '
                             '%s' % type(access_token))

        if access_token and (not access_token['access_token']):
            raise ValueError('Invalid token: Missing "access_token" in '
                             '"self.access_token".')

        self.access_token = access_token
        self.file_put_contents(access_token)

    def get_access_token(self):
        """
        Get and return :code:`access_token` from config.

        Returns:
            str: :code:`access_token`
        """
        return self.access_token['access_token']

    def is_access_token_expired(self):
        """
        Return :code:`True`, if :code:`access_token` expired else
        :code:`False` depending on the :code:`created` and
        :code:`expires_in` dates.

        Returns:
            bool: True or False depending on date
        """
        if not self.access_token:
            return True

        created = 0
        expires_in = 0

        if self.access_token['created']:
            created = self.access_token['created']

        if self.access_token['expires_in']:
            expires_in = self.access_token['expires_in']

        # created + ~4 hours
        diff = created + datetime.timedelta(seconds=expires_in - 30)
        # are 4 hours passed since creation date?
        expired = diff < datetime.datetime.now()
        return expired

    def get_refresh_token(self):
        """
        Return the refresh_token that was saved in our local file during
        authentication.

        Returns:
            str: :code:`refresh_token` from this class
        """
        if self.access_token and self.access_token['refresh_token']:
            return self.access_token['refresh_token']

    def fetch_access_token_with_auth_code(self, code):
        """
        Get a code and create an `access_token` from that code.

        Args:
            code (str): the code that we receive in our URL once authenticated

        Returns:
            dict: :code:`access_token` data
        """
        if not code:
            raise Exception("Invalid code")

        auth = self.get_oauth2_service()
        auth.set_code(code)
        auth.set_redirect_uri(self.get_redirect_uri())

        credentials = auth.fetch_auth_token()
        if credentials and credentials['access_token']:
            credentials['created'] = datetime.datetime.now()
            self.set_access_token(credentials)

        return credentials

    def refresh_token(self, refresh_token=''):
        """
        Get an (optional) `refresh_token` and create a new 'access_token'
        from that.

        .. note::
            It's imporant to set the :code:`grant_type` to
            **refresh_token** with
            :code:`OAuth2().set_grant_type('refresh_token')`.

        Returns:
            dict: :code:`access_token` data on success

        Raises:
            ValueError: if no :code:`refresh_token` can be found or the
                token could not be processed correctly.
        """
        print("refreshing token...\n")
        if not refresh_token:
            if not self.access_token['refresh_token']:
                raise ValueError('Refresh token must be passed or set as part '
                                 'of the access_token')

            refresh_token = self.access_token['refresh_token']

        auth = self.get_oauth2_service()
        auth.set_grant_type('refresh_token')  # important!
        auth.set_refresh_token(refresh_token)

        credentials = auth.fetch_auth_token()

        if credentials and credentials['access_token']:
            credentials['created'] = datetime.datetime.now()
            if not credentials['refresh_token']:
                credentials['refresh_token'] = refresh_token
            self.set_access_token(credentials)
            print("successfully refreshed token...\n")
            return credentials

        raise ValueError('Illegal access token received when token was '
                         'refreshed')

    def get_oauth2_service(self):
        """
        Instantiate the OAuth2 service to be used for authentication.

        Returns:
            class: :class:`~bexiopy.api.OAuth2` instance
        """
        if not self.auth:
            self.auth = OAuth2(**{
                'client_id': self.get_client_id(),
                'client_secret': self.get_client_secret(),
                'authorization_uri': self.OAUTH2_AUTH_URL,
                'token_credential_uri': self.OAUTH2_TOKEN_URI,
                'refresh_token_credential_uri': self.OAUTH2_REFRESH_TOKEN_URI,
                'refresh_token': self.get_refresh_token(),
                'redirect_uri': self.get_redirect_uri(),
                'issuer': self.config['client_id']
            })
        return self.auth

    def get_oauth2_auth_url(self):
        """
        Return the URL for authentication with Bexio.

        Returns:
            str: URL for verifying the account
        """
        params = {
            'client_id': self.config['client_id'],
            'client_secret': self.config['client_secret'],
            'redirect_uri': self.config['redirect_uri'],
            'scope': self.config['scope'],
            'state': self.config['state']
        }
        redirect_to = self.OAUTH2_AUTH_URL + '?' + urlencode(params)
        return redirect_to

    def get_request_headers(self):
        """
        Return the headers needed to make a regular request, given we
        are already authenticated.

        Returns:
            dict: map of request headers
        """
        return {
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + self.get_access_token()
        }

    def load_access_token_from_file(self):
        """
        Open and return the dictionary of the shelve file.

        Returns:
            dict: :code:`access_token` loaded from file
        """
        token_file = get_setting('BEXIO_CREDENTIALS_FILENAME')
        if os.path.exists(token_file):
            access_token = shelve.open(token_file)
            token = dict(access_token)
            access_token.close()
            self.access_token = token
        else:
            # let user know, he needs to authentiate with bexio
            print(
                "You need to authorize this app with your "
                "bexio instance. Open the following link and "
                "you will be redirected back.\n\n%s" %
                self.get_oauth2_auth_url())
            self.access_token = {}
        return self.access_token

    def call(self, method, path, data={}):
        """
        Get `method`, `path` and optionally `data`, make a request
        to the Bexio API and return the resonse as `json`.

        Usage:

        .. code-block:: python

            call('POST', 'salutation', {'param1': 'test'})
            call('GET', 'salutation')

        Args:
            method (str): The request method to use ('GET', 'POST', etc.)
            path (str): The endpoint for the API call
            data (dict): Data for 'POST' and other requests

        Returns:
            dict: The response of the request (:code:`response.json()`)
        """
        if not self.access_token:
            return ('You must authenticate with Bexio. Open the following '
                    'URL and authenticate: \n\n %s' %
                    self.get_oauth2_auth_url())

        if self.is_access_token_expired():
            print("\n\nTOKEN EXPIRED!\n\n")
            self.refresh_token()

        kwargs = {
            'headers': self.get_request_headers()
        }

        if data:
            if isinstance(data, (dict, list)):
                import json
                data = json.dumps(data)
            kwargs.update({
                'data': data
            })
        url = self.API_URL + '/' + self.get_org() + '/' + path
        print('\n%s: %s\n' % (method.upper(), url))
        response = getattr(requests, method.lower())(url, **kwargs)

        return response.json()


class Bexiopy(object):
    """
    The class to be used to query the Bexio API. Each resource is available
    via this class.

    See API Resources section for available queries.
    """
    contacts = contacts.ContactsResource()
    invoices = invoices.InvoicesResource()
    general = general.GeneralResource()
