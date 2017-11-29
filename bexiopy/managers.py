# -*- coding: utf-8 -*-
from __future__ import absolute_import

from . import api


class BaseManager:
    @property
    def api(self):
        return api.Bexiopy()

    def all(self):
        return self.api.call(
            endpoint=self.endpoint)

    def get(self, oid=None):
        return self.api.call(
            endpoint=self.endpoint, oid=oid)

    def create(self, **data):
        return self.api.call(
            endpoint=self.endpoint, method="POST", data=data)

    def update(self, oid=None, **data):
        return self.api.call(
            endpoint=self.endpoint, method="PUT", data=data, oid=oid)

    def update_or_create(self, oid=None, **data):
        return self.update(oid=oid, **data) if oid else self.create(**data)


class InvoicesManager(BaseManager):
    endpoint = 'kb_invoice'

    def make_payment(self, oid, amount):
        """
        Not working API wise yet! Should record payment on invoice.
        """
        subendpoint = 'payment'
        data = {
            'value': amount,
        }
        self.api.call(
            endpoint=self.endpoint, method="POST", data=data,
            subendpoint=subendpoint, oid=oid)


class ContactsManager(BaseManager):
    endpoint = 'contact'
