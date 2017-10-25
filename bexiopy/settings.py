# -*- coding: utf-8 -*-
from django.conf import settings


def get_setting(name):
    """
    Receive a name and try to return the corresponding setting. The
    settings defined in the root settings of your django project have
    priority over defaults.

    Define your defaults here.
    """
    # define these in your settings
    _BEXIO_CLIENT_SECRET = ''
    _BEXIO_CLIENT_ID = ''
    _BEXIO_APPLICATION_SCOPES = []
    _BEXIO_APPLICATION_REDIRECTION_URL = ''

    # adjust if necessary
    _BEXIO_AUTH_URL = 'https://office.bexio.com/oauth/authorize'
    _BEXIO_TOKEN_URL = 'https://office.bexio.com/oauth/access_token'
    _BEXIO_TOKEN_REFRESH_URL = 'https://office.bexio.com/oauth/refresh_token'
    _BEXIO_API_URL = 'https://office.bexio.com/api2.php'
    _BEXIO_CREDENTIALS_FILENAME = '.bxcred'

    defaults = {
        'BEXIO_AUTH_URL': getattr(
            settings,
            'BEXIO_AUTH_URL',
            _BEXIO_AUTH_URL
        ),
        'BEXIO_CLIENT_ID': getattr(
            settings,
            'BEXIO_CLIENT_ID',
            _BEXIO_CLIENT_ID
        ),
        'BEXIO_CLIENT_SECRET': getattr(
            settings,
            'BEXIO_CLIENT_SECRET',
            _BEXIO_CLIENT_SECRET
        ),
        'BEXIO_APPLICATION_SCOPES': ' '.join(
            getattr(
                settings,
                'BEXIO_APPLICATION_SCOPES',
                _BEXIO_APPLICATION_SCOPES
            )
        ),
        'BEXIO_APPLICATION_REDIRECTION_URL': getattr(
            settings,
            'BEXIO_APPLICATION_REDIRECTION_URL',
            _BEXIO_APPLICATION_REDIRECTION_URL
        ),
        'BEXIO_API_URL': getattr(
            settings,
            'BEXIO_API_URL',
            _BEXIO_API_URL
        ),
        'BEXIO_TOKEN_URL': getattr(
            settings,
            'BEXIO_TOKEN_URL',
            _BEXIO_TOKEN_URL
        ),
        'BEXIO_TOKEN_REFRESH_URL': getattr(
            settings,
            'BEXIO_TOKEN_REFRESH_URL',
            _BEXIO_TOKEN_REFRESH_URL
        ),
        'BEXIO_CREDENTIALS_FILENAME': getattr(
            settings,
            'BEXIO_CREDENTIALS_FILENAME',
            _BEXIO_CREDENTIALS_FILENAME
        ),
    }
    return defaults[name]
