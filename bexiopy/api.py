# -*- coding: utf-8 -*-
import requests
import json
import shelve
import os

try:
    # For Python 3.0 and later
    from urllib.parse import urlencode
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib import urlencode

from .managers import InvoicesManager, ContactsManager
from .settings import get_setting
from .models import BexioSession


class BexiopyBase(object):

    def __init__(self, *args, **kwargs):
        super(BexiopyBase, self).__init__(*args, **kwargs)

    @staticmethod
    def get_authentication_url():
        """
        Return the authentication URL build from Bexiopy settings. You
        can modify the settings in order to build your own authentication
        URL. Check the Bexio docs for more details.
        """
        base_url = get_setting('BEXIO_AUTH_URL')
        params = {
            'client_id': get_setting('BEXIO_CLIENT_ID'),
            'scope': get_setting('BEXIO_APPLICATION_SCOPES'),
            'client_secret': get_setting('BEXIO_CLIENT_SECRET'),
            'redirect_uri': get_setting('BEXIO_APPLICATION_REDIRECTION_URL'),
            'state': 'SOME_RANDOM_SEQUENCE',
        }
        params_encoded = urlencode(params)
        return base_url + '/?' + params_encoded

    def _load_tokens_from_file(self):
        """
        Open and return the dictionary of the shelve file.
        """
        file = get_setting('BEXIO_CREDENTIALS_FILENAME')
        if os.path.exists(file):
            d = shelve.open(file)
            print(d)
            if ('access_token' in d) and ('org' in d):
                self.organization_id = d['org']
                self.access_token = d['access_token']
                self.refresh_token = d['refresh_token']
                self.scope = d['scope']
                return True
        else:
            # let user know, he needs to authentiate with bexio
            raise ValueError("You need to authorize this app with your "
                             "bexio instance. Open the following link and "
                             "you will be redirected back.\n\n%s" %
                             self.get_authentication_url())
        return False

    def get_headers(self):
        self._load_tokens_from_file()
        HEADERS = {
            'Accept': 'application/json',
            'Authorization': 'Bearer %s' % self.access_token
        }
        return HEADERS

    def get_api_url(self, endpoint=""):
        self._load_tokens_from_file()
        url = os.path.join(
            get_setting('BEXIO_API_URL'), self.organization_id, endpoint)
        return url


class BexiopyAuth(BexiopyBase):
    """
    This is the main class used to communicate withe the Bexio API. It
    authenticates the instance with bexio so you can access the data
    through the api.

    After authentication, you can use the API through an ORM similar to
    Django. If you know Django well, you should be comfortable with using
    it.

    Auth flow:
        - Check, if we have a session stored already
            - yes:
                - try connection with those credentials
                - if it works, return success
            - no:
                - create initial auth via link
                - credentials

    """
    _AUTH_FAILURE_MESSAGE = 'Authentication failed!'
    _AUTH_SUCCESS_MESSAGE = 'Authentication success.'

    AUTH_RESPONSES = {
        200: {
            'status': 200,
            'message': _AUTH_SUCCESS_MESSAGE
        },
        'default': {
            'status': 500,
            'message': _AUTH_FAILURE_MESSAGE
        }
    }

    def get_or_create_state(self):
        """
        Check, if we have a state already. If not, create a new one.
        The state is needed to authenticate with bexio.
        """
        return

    def get_api_access_token(self, code):
        """
        Response:
        ```
        {
            "access_token": "a24267sdzfsdzf978zds98za",
            "expires_in": 14400,
            "token_type": "Bearer",
            "scope": "kb_invoice_show kb_invoice_edit general",
            "refresh_token": "aasdiuha239h",
            "org": "j8us8df8sdhf8",
            "user_id": 1
        }
        ```
        """
        url = get_setting('BEXIO_TOKEN_URL')
        params = {
            'client_id': get_setting('BEXIO_CLIENT_ID'),
            'client_secret': get_setting('BEXIO_CLIENT_SECRET'),
            'redirect_uri': get_setting('BEXIO_APPLICATION_REDIRECTION_URL'),
            'code': code
        }
        response = requests.post(url, params=params)

        if response.status_code == 200:
            self._write_credentials_to_file(response.json())
        else:
            raise UserWarning(response.content)
        return response

    def refresh_token(self):
        url = get_setting('BEXIO_TOKEN_REFRESH_URL')
        params = {
            'client_id': get_setting('BEXIO_CLIENT_ID'),
            'client_secret': get_setting('BEXIO_CLIENT_SECRET'),
            'refresh_token': self._load_tokens_from_file().refresh_token
        }
        response = requests.post(url, params=params)
        self.access_token = response.json()
        """
        {
            "access_token": "2f53ebba4711458cb8b7ce0c0666d7cf83339c4a",
            "expires_in": 14400,
            "token_type": "Bearer",
            "scope": "kb_invoice_show kb_invoice_edit general",
            "refresh_token": "biolao9aF5XtRwY5TBt/3u86vrBgiN6IGJFFNEunx6E=",
            "org": "iavg8nyaedlw",
            "user_id": 1
        }
        """
        return response

    def has_authenticated(self, code, state):
        return False

    def _write_credentials_to_file(self, data):
        """
        Write response data into a shelve file, which is basically a locally
        stored dictionary.

        Input:

            data : dict, dictionary of the response content
        """
        d = shelve.open(get_setting('BEXIO_CREDENTIALS_FILENAME'))

        # write json to file
        for k, v in data.items():
            d[k] = v

        # closing is important!
        d.close()


class Bexiopy(BexiopyBase):

    invoices = InvoicesManager()
    contacts = ContactsManager()

    def __init__(self, *args, **kwargs):
        super(Bexiopy, self).__init__(*args, **kwargs)

    def make_request(
            self, endpoint="", method="GET", oid=None, data={}):
        if not endpoint:
            raise ValueError('Enpoint is missing for function Bexiopy.'
                             'make_request. Please provide a proper '
                             'endpoint for the api request.')
        response = None
        url = self.get_api_url(endpoint)
        # append object id to url, for specific object queries
        if oid:
            url = os.path.join(url, str(oid))

        if method == "GET":
            response = requests.get(url, headers=self.get_headers())

        elif method == "POST":
            if not data:
                raise ValueError(
                    'Data argument is missing. Please provide '
                    'a dictionary for this function.')

            response = requests.post(
                url, headers=self.get_headers(), data=json.dumps(data))
        print(url)
        return response
