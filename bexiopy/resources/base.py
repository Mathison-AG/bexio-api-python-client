# -*- coding: utf-8 -*-
from __future__ import absolute_import

from ..helpers import concatenate_path_pk as _c


class BaseClientResource(object):
    """
    Base client resource that instantiates the :class:`~bexiopy.api.Client`.
    """
    def __init__(self, *args, **kwargs):
        from ..api import Client
        self.client = Client()


class BaseResource(BaseClientResource):
    """
    Base resource that's inherited by all other resources.

    Inheriting classes may have additional methods, that are resource
    specific. Take a look at the resources to find these additional
    methods.

    Attributes:
        ENDPOINT (str): the endpoint that should be queried
        ENDPOINT_SEARCH (str): the serach endpoint that should be queried
    """
    def __init__(self, *args, **kwargs):
        super(BaseResource, self).__init__(*args, **kwargs)
        if not any([self.ENDPOINT, self.ENDPOINT_SEARCH]):
            raise ValueError('Please provide an endpoint and a '
                             'search_endpoint for the class inheriting '
                             'BaseResource.')

    def all(self):
        """
        Get all objects of given endpoint.

        Returns:
            list: List of all objects from requested endpoint
        """
        return self.client.call('GET', self.ENDPOINT)

    def search(self, params=[]):
        """
        Search for specific object and return response.

        Args:
            params (dict): Parameters to narrow down the search

        Returns:
            list: List of results from request
        """
        return self.client.call('POST', self.ENDPOINT_SEARCH, params)

    def create(self, data):
        """
        Add new object.

        Args:
            data (dict): Dictionary object with appropriate data

        Returns:
            dict: Object that has been created
        """
        return self.client.call('POST', self.ENDPOINT, data)

    def get(self, pk):
        """
        Get specific object.

        Args:
            pk (str): Bexio id of object

        Returns:
            dict: Object that has been pulled
        """
        path = _c(self.ENDPOINT, pk)
        return self.client.call('GET', path, {})

    def update(self, pk, data):
        """
        Update existing object.

        Args:
            pk (str): Bexio id of object
            data (dict): Data that should be updated

        Returns:
            dict: Object that has been updated
        """
        path = _c(self.ENDPOINT, pk)
        return self.client.call('POST', path, data)

    def delete(self, pk):
        """
        Delete object.

        Args:
            pk (str): Bexio id of object

        Returns:
            dict: Response dictionary of operation
        """
        path = _c(self.ENDPOINT, pk)
        return self.client.call('DELETE', path)

    def overwrite(self, pk, data):
        """
        Add new contact

        Args:
            pk (str): Bexio id of object
            data (dict): Data that should be overwritten

        Returns:
            dict: Object that has been overwritten
        """
        path = _c(self.ENDPOINT, pk)
        return self.client.call('PUT', path, data)
