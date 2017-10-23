# -*- coding: utf-8 -*-

try:
    # For Python 3.0 and later
    from urllib.parse import urlencode
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib import urlencode

from .settings import get_setting


class BexiopyAuth(object):
    """
    This is the main class used to communicate withe the Bexio API. It
    authenticates the instance with bexio so you can access the data
    through the api.

    After authentication, you can use the API through an ORM similar to
    Django. If you know Django well, you should be comfortable with using
    it.
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

    def __init__(self, *args, **kwargs):
        super(BexiopyAuth, self).__init__(*args, **kwargs)

    def authenticate(self):
        auth_url = self.get_authentication_url()
        return auth_url

    def get_authentication_url(self):
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
            'state': self.get_or_create_state(),
        }
        params_encoded = urlencode(params)
        return base_url + '/?' + params_encoded

    def get_or_create_state(self):
        """
        Check, if we have a state already. If not, create a new one.
        The state is needed to authenticate with bexio.
        """
        return

    def callback(self):
        return

    def has_authenticated(self, code, state):
        return True
