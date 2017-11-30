#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_bexio-api-python-client
------------

Tests for `bexio-api-python-client` models module.
"""

from django.test import TestCase

from bexiopy import api, settings


class TestBexiopy(TestCase):

    def setUp(self):
        self.client = api.Client()
        self.bexio = api.Bexiopy()

    def test_client_init(self):
        # check if client has correct client id
        self.assertEqual(
            self.client.get_client_id(),
            settings.get_setting('BEXIO_CLIENT_ID')
        )

        self.assertEqual(
            self.client.get_client_secret(),
            settings.get_setting('BEXIO_CLIENT_SECRET')
        )

        self.assertEqual(
            self.client.get_redirect_uri(),
            settings.get_setting('BEXIO_APPLICATION_REDIRECTION_URL')
        )

        self.assertEqual(
            self.client.config['scope'],
            settings.get_setting('BEXIO_APPLICATION_SCOPES')
        )

        self.assertEqual(
            self.client.get_client_id(),
            settings.get_setting('BEXIO_CLIENT_ID')
        )

        self.assertEqual(
            self.client.API_URL,
            settings.get_setting('BEXIO_API_URL')
        )

        self.assertEqual(
            self.client.OAUTH2_AUTH_URL,
            settings.get_setting('BEXIO_AUTH_URL')
        )

        self.assertEqual(
            self.client.OAUTH2_TOKEN_URI,
            settings.get_setting('BEXIO_TOKEN_URL')
        )

        self.assertEqual(
            self.client.OAUTH2_REFRESH_TOKEN_URI,
            settings.get_setting('BEXIO_TOKEN_REFRESH_URL')
        )

    def tearDown(self):
        pass
