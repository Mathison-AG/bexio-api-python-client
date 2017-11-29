# -*- coding: utf-8 -*-
from __future__ import absolute_import

from ..helpers import concatenate_path_pk as _c
from .base import BaseResource


class InvoicesResource(BaseResource):
    """
    Resource to query the contacts endpoint.
    """
    endpoint = 'kb_invoice'
    search_endpoint = 'kb_invoice/search'

    def show_pdf(self, pk):
        """
        Return the PDF version of a given invoice.

        :param: pk, bexio id of invoice
        :return: mixed
        """
        path = _c(self.endpoint, pk, 'pdf')
        return self.client.call('GET', path)

    def copy(self, pk, data):
        """
        Return the PDF version of a given invoice.

        :param: pk, bexio id of invoice
        :return: mixed
        """
        path = _c(self.endpoint, pk, 'copy')
        return self.client.call('POST', path, data)
