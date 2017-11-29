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
        self.config['refresh_token'] = refresh_token

    def get_refresh_token(self):
        return self.config['refresh_token']

    def get_client_id(self):
        return self.config['client_id']

    def set_client_id(self, client_id):
        self.config['client_id'] = client_id

    def get_client_secret(self):
        return self.config['client_secret']

    def set_client_secret(self, client_secret):
        self.config['client_secret'] = client_secret

    def get_code(self):
        return self.config['code']

    def set_code(self, code):
        self.config['code'] = code

    def get_redirect_uri(self):
        return self.config['redirect_uri']

    def set_redirect_uri(self, redirect_uri):
        self.config['redirect_uri'] = redirect_uri

    def get_grant_type(self):
        if self.grant_type:
            return self.grant_type

        if not self.config['code']:
            return 'authorization_code'

        elif not self.config['refresh_token']:
            return 'refresh_token'

        elif ((not self.config['username']) and (not self.config['password'])):
            return 'password'

        else:
            return None

    def set_grant_type(self, grant_type):
        self.grant_type = grant_type

    def fetch_auth_token(self):
        return self.generate_credentials_request()

    def generate_credentials_request(self):
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
        return self.config['token_credential_uri']

    def get_refresh_token_credential_uri(self):
        return self.config['refresh_token_credential_uri']

    def add_client_credentials(self, params):
        params['client_id'] = self.get_client_id()
        params['client_secret'] = self.get_client_secret()

        return params


class Client(object):
    API_URL = 'https://office.bexio.com/api2.php'
    OAUTH2_AUTH_URL = 'https://office.bexio.com/oauth/authorize'
    OAUTH2_TOKEN_URI = 'https://office.bexio.com/oauth/access_token'
    OAUTH2_REFRESH_TOKEN_URI = 'https://office.bexio.com/oauth/refresh_token'

    # Client constructor
    def __init__(self, *args, **kwargs):
        self.auth = None
        self.config = {
            'client_id': get_setting('BEXIO_CLIENT_ID'),
            'client_secret': get_setting('BEXIO_CLIENT_SECRET'),
            'redirect_uri': get_setting('BEXIO_APPLICATION_REDIRECTION_URL'),
            'scope': get_setting('BEXIO_APPLICATION_SCOPES'),
            'state': uuid.uuid4()
        }
        self.load_access_token_from_file()

    def set_client_id(self, client_id):
        self.config['client_id'] = client_id

    def get_client_id(self):
        return self.config['client_id']

    def set_client_secret(self, client_id):
        self.config['client_id'] = client_id

    def get_client_secret(self):
        return self.config['client_secret']

    def set_redirect_uri(self, redirect_uri):
        self.config['redirect_uri'] = redirect_uri

    def get_redirect_uri(self):
        return self.config['redirect_uri']

    def get_org(self):
        return self.access_token['org']

    def file_put_contents(self, access_token):
        """
        Write response data into a shelve file, which is basically a locally
        stored dictionary.

        Input:

            :access_token: dict, access token dict we receive from bexio
        """
        d = shelve.open(get_setting('BEXIO_CREDENTIALS_FILENAME'))

        # write json to file
        for k, v in access_token.items():
            d[k] = v

        # closing is important!
        d.close()

    def set_access_token(self, access_token):
        """
        :param: access_token
        :@throws: \Exception
        """
        if not isinstance(access_token, dict):
            raise Exception('Invalid token format: Need dict instead of '
                            '%s' % type(access_token))

        if access_token and (not access_token['access_token']):
            raise Exception("Invalid token: Missing 'access_token' in "
                            "'self.access_token'.")

        self.access_token = access_token
        self.file_put_contents(access_token)

    def get_access_token(self):
        return self.access_token['access_token']

    def is_access_token_expired(self):
        """
        Return `True`, if `access_token` expired else `False` depending
        on the `created` and `expires_in` dates.

        :return: bool, True or False depending on date
        """
        if not self.access_token:
            return True

        created = 0
        expires_in = 0

        if self.access_token['created']:
            created = self.access_token['created']

        if self.access_token['expires_in']:
            expires_in = self.access_token['expires_in']

        return (
            created +
            datetime.timedelta(expires_in - 30) <
            datetime.datetime.now()
        )

    def get_refresh_token(self):
        """
        Return the refresh_token that was saved in our local file during
        authentication.

        :return: str, access_token from this class
        """
        if self.access_token and self.access_token['refresh_token']:
            return self.access_token['refresh_token']

    def fetch_auth_code(self):
        auth = self.get_oauth2_service()
        auth.set_redirect_uri(self.get_redirect_uri())

    def fetch_access_token_with_auth_code(self, code):
        """
        Get a code and create an `access_token` from that code.

        :return: dict, access_token data
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

        Note: It's imporant to set the `grant_type` to 'refresh_token' with
        `OAuth2.set_grant_type('refresh_token')`.

        :return: dict, access_token data
        :return: Exception, if credentials cannot be processed correctly
        """
        print("refreshing token...\n")
        if not refresh_token:
            if not self.access_token['refresh_token']:
                raise Exception('Refresh token must be passed or set as part '
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

        raise Exception('Illegal access token received when token was '
                        'refreshed')

    def get_oauth2_service(self):
        """
        Instantiate the OAuth2 service to be used for authentication.

        :return: OAuth2()
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

        :return: str, URL for verifying the account
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

        :return: dict, map of request headers
        """
        return {
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + self.get_access_token()
        }

    def load_access_token_from_file(self):
        """
        Open and return the dictionary of the shelve file.

        :return: dict, access_token loaded from file
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
            call('POST', 'salutation', {'param1': 'test'})
            call('GET', 'salutation')

        :param: method, the request method used ('GET', 'POST', etc.)
        :param: path, the endpoint for the API call
        :param: params (optional), data for 'POST' and other requests
        :return: json, the response of the request
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
            kwargs.update({
                'data': data
            })
        url = self.API_URL + '/' + self.get_org() + '/' + path
        print('\nRequesting: %s\n' % url)
        response = getattr(requests, method.lower())(url, **kwargs)

        return response.json()


class Bexiopy(object):
    """
    The class to be used to query the Bexio API.

    Usage:

        api = Bexiopy()

        # get all contacts
        contacts = api.get_contacts()

        # create a contact
        api.create_contact(params={'attr1': 'val1', 'attr2': 'val2'})

        # search a contact
        contact = api.search_contacts(params={'param1': 'some value'})

        # get one specific contact with id 2
        contact = api.get_contact(2)

    See API Resources section for available queries.
    """
    contacts = contacts.ContactsResource()
    invoices = invoices.InvoicesResource()
    general = general.GeneralResource()
