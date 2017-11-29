# -*- coding: utf-8 -*-
try:
    from django.conf import settings
    try:
        settings.configure()  # for autodocs
    except RuntimeError:
        pass
except ImportError:
    settings = {}


ALL_SCOPES = [
    'general',
    'kb_invoice_edit',
    'contact_edit',
    'article_edit',
    'kb_order_edit',
]


def get_setting(name):
    """
    Receive a name and try to return the corresponding setting.

    Args:
        name (str): name of setting

    Returns:
        mixed: value of requested setting

    **Django**

    The settings defined in the root settings of your django project have
    priority over defaults.

    **Python**

    If you use the API without Django, you can define the settings in
    this file. Just add the following to the top of the file with your
    settings:

    .. code-block:: python

        settings = {
            'BEXIO_AUTH_URL': '...',
            'BEXIO_CLIENT_ID': '...',
            'BEXIO_CLIENT_SECRET': '...',
            ...
        }

    """
    # define these in your settings
    _BEXIO_CLIENT_SECRET = ''
    _BEXIO_CLIENT_ID = ''
    _BEXIO_APPLICATION_REDIRECTION_URL = ''

    # adjust if necessary
    _BEXIO_APPLICATION_SCOPES = ALL_SCOPES
    _BEXIO_AUTH_URL = 'https://office.bexio.com/oauth/authorize'
    _BEXIO_TOKEN_URL = 'https://office.bexio.com/oauth/access_token'
    _BEXIO_TOKEN_REFRESH_URL = 'https://office.bexio.com/oauth/refresh_token'
    _BEXIO_API_URL = 'https://office.bexio.com/api2.php'
    _BEXIO_CREDENTIALS_FILENAME = '.bxcred'

    defaults = {
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
        'BEXIO_AUTH_URL': getattr(
            settings,
            'BEXIO_AUTH_URL',
            _BEXIO_AUTH_URL
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
