# -*- coding: utf-8 -*-
from __future__ import absolute_import

from .base import BaseResource


class ContactsResource(BaseResource):
    """
    Resource to query the contacts endpoint.

    Endpoint Docs:

        https://docs.bexio.com/ressources/contact/

    Examples:

    .. code-block:: python

        bexio = Bexiopy()

        # get all contacts
        contacts = bexio.contacts.all()

        # create an invoice
        contact = bexio.invoices.create(params={'attr1': 'val1', ...)

        # search a contact
        contact = bexio.contacts.search(params={'param1': 'some value'})

        # get one specific contact with id 2
        contact = bexio.contacts.get(pk=2)
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
