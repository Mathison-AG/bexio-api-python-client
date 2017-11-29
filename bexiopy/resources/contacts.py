# -*- coding: utf-8 -*-
from __future__ import absolute_import

from .base import BaseResource


class ContactsResource(BaseResource):
    """
    Resource to query the contacts endpoint.
    """
    endpoint = 'contact'
    search_endpoint = 'contact/search'

    def get_relations(self):
        """
        Get relations from contacts

        :return: mixed
        """
        return self.client.call('GET', 'contact_relation', {})
