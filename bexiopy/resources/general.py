# -*- coding: utf-8 -*-
from __future__ import absolute_import

from .base import BaseClientResource


class GeneralResource(BaseClientResource):
    """
    Resource to get general information about your Bexio instance.
    """
    def get_salutations(self):
        """
        Get available salutations

        :return: mixed
        """
        return self.client.call('GET', 'salutation', {})

    def get_titles(self):
        """
        Get available titles

        :return: mixed
        """
        return self.client.call('GET', 'title', {})
