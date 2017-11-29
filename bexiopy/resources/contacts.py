# -*- coding: utf-8 -*-
from __future__ import absolute_import

from .base import BaseResource


class ContactsResource(BaseResource):
    """
    Resource to query the contacts endpoint.

    Endpoint Docs:

        https://docs.bexio.com/ressources/contact/
    """
    ENDPOINT = 'contact'
    ENDPOINT_SEARCH = 'contact/search'

    def get_relations(self):
        """
        Get relations from contacts

        Returns:
            list: List of contact relations
        """
        return self.client.call('GET', 'contact_relation', {})
