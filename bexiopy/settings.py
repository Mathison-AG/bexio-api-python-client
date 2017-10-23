# -*- coding: utf-8 -*-
from django.conf import settings


def get_setting(name):
    """
    Receive a name and try to return the corresponding setting. The
    settings defined in the root settings of your django project have
    priority over defaults.

    Define your defaults here.
    """
    _BEXIO_AUTH_URL = 'https://office.bexio.com/oauth/authorize'
    _BEXIO_CLIENT_ID = '9170616879.apps.bexio.com'
    _BEXIO_CLIENT_SECRET = 'WbH5Di/6g+Te+cIElwJZI3jYMdo='
    _BEXIO_TOKEN_URL = 'https://office.bexio.com/oauth/access_token'
    _BEXIO_API_URL = 'https://office.bexio.com/api2.php'

    _BEXIO_APPLICATION_SCOPES = ['kb_invoice_edit', ]
    _BEXIO_APPLICATION_REDIRECTION_URL = 'http://localhost:8001/auth/'

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
        'BEXIO_APPLICATION_SCOPES': ','.join(
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

    }
    return defaults[name]
"""
state=_ae5fd8d6c69d6f72708dbbce723aa9dd38390af373:http://my.bexio.com/simplesaml/saml2/idp/SSOService.php?spentityid=easysys%26amp;cookieTime=1508419466
"""