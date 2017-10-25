# -*- coding: utf-8 -*-
import requests
import json
import os

from .settings import get_setting

import api


class InvoicesManager:
    endpoint = 'kb_invoice'

    def get(self, oid=None, pdf=False):
        return api.Bexiopy().make_request(self.endpoint)

    def create(self):
        return "InvoicesManager.create()"

    def all(self):
        return "InvoicesManager.all()"


class ContactsManager:
    endpoint = 'contact'

    def all(self):
        return api.Bexiopy().make_request(
            self.endpoint, )

    def get(self, oid=None, pdf=False):
        return api.Bexiopy().make_request(self.endpoint, oid=oid)

    def create(self, **data):
        return api.Bexiopy().make_request(
            self.endpoint, method="POST", data=data)

    def update(self, oid=None, **data):
        return api.Bexiopy().make_request(
            self.endpoint, method="POST", oid=oid, data=data)

    def update_or_create(self, oid=None, **data):
        if oid:
            return self.update(oid=oid, **data)
        else:
            return self.create(**data)
