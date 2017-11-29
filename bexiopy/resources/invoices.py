# -*- coding: utf-8 -*-
from __future__ import absolute_import

from ..helpers import concatenate_path_pk as _c
from .base import BaseResource


class InvoicesResource(BaseResource):
    """
    Resource to query the contacts endpoint.

    Endpoint Docs:

        https://docs.bexio.com/ressources/kb_invoice/
    """
    ENDPOINT = 'kb_invoice'
    ENDPOINT_SEARCH = 'kb_invoice/search'

    def show_pdf(self, pk):
        """
        Return the PDF version of a given invoice. Needs to be further
        processed so you can extract the file from the response.

        Args:
            pk (str): Bexio id of invoice

        Returns:
            file: PDF file of invoice
        """
        path = _c(self.endpoint, pk, 'pdf')
        return self.client.call('GET', path)

    def copy(self, pk, data):
        """
        Return the PDF version of a given invoice.

        Args:
            pk (str): Bexio id of invoice

        Returns:
            dict: Invoice that was copied
        """
        path = _c(self.endpoint, pk, 'copy')
        return self.client.call('POST', path, data)
