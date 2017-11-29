# -*- coding: utf-8 -*-
from __future__ import absolute_import

from ..helpers import concatenate_path_pk as _c


class BaseClientResource(object):
    """
    Base client resource that instantiates a Client() class.
    """
    def __init__(self, *args, **kwargs):
        from ..api import Client
        self.client = Client()


class BaseResource(BaseClientResource):
    """
    Base resource that's inherited by all other resources.

    Methods:

        all        : get all the objects of the endpoint
        search     : search for a particular object
        get        : get a specific object
        create     : create an object

    Inheriting classes may have additional methods, that are resource
    specific. Take a look at the resources to find these additional
    methods.
    """
    def __init__(self, *args, **kwargs):
        super(BaseResource, self).__init__(*args, **kwargs)
        if not any([self.endpoint, self.search_endpoint]):
            raise ValueError('Please provide an endpoint and a '
                             'search_endpoint for the class inheriting '
                             'BaseResource.')

    def all(self):
        """
        Get all objects of given endpoint.

        :return: dict
        """
        return self.client.call('GET', self.endpoint)

    def search(self, params={}):
        """
        Search for specific object.

        :param: dict, search params
        :return: mixed
        """
        return self.client.call('POST', self.search_endpoint, params)

    def create(self, data):
        """
        Add new object.

        :param: data, `params` dict
        :return: mixed
        """
        return self.client.call('POST', self.endpoint, data)

    def get(self, pk):
        """
        Get specific object.

        :param: pk, id of bexio object (bexio id)
        :return: mixed, response from Bexio API request
        """
        path = _c(self.endpoint, pk)
        return self.client.call('GET', path, {})

    def update(self, pk, data):
        """
        Update existing object.

        :param: pk, id of bexio object (bexio id)
        :param: data, dict with data that should be updated
        :return: mixed
        """
        return self.client.call('POST', self.endpoint, data)

    def delete(self, pk):
        """
        Delete object.

        :param: pk, id of bexio object (bexio id)
        :return: mixed
        """
        path = _c(self.endpoint, pk)
        return self.client.call('DELETE', path)

    def overwrite(self, pk, data):
        """
        Add new contact

        :param: pk, id of bexio object (bexio id)
        :param: data, dict with data that should be overwritten
        :return: mixed
        """
        path = _c(self.endpoint, pk)
        return self.client.call('PUT', path, data)
