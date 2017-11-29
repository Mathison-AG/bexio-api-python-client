# -*- coding: utf-8 -*-
from django.db import models


class BexiopyModelMixin(models.Model):
    """
    Base model mixin for django models. Add as last class, so it does not
    override any default settings of your model.
    """
    bexio_id = models.IntegerField(
        verbose_name='bexio ID',
        null=True, blank=True)

    @property
    def bexio_api(self):
        from bexiopy.api import Bexiopy
        return Bexiopy()

    def bexio_contact_sync(self):
        contact_data = {
            'contact_type_id': 1,
            'name_1': self.user.name,
            'owner_id': 1,
            'user_id': 1
        }
        contact = self.bexio_api.contacts.update_or_create(
            oid=self.user.bexio_id, **contact_data)
        self.user.bexio_id = contact.json().get('id')
        self.user.save()
        return contact

    def bexio_invoice_sync(self):
        """
        Creates an invoice in Bexio, if object does not have a `bexio_id`.

        :return: requests response object or `None`
        """

        if self.bexio_id:
            return

        # check if we already have a contact in bexio, else create
        if not self.user.bexio_id:
            self.bexio_contact_sync()

        # invoice data
        invoice_data = {
            'contact_id': self.user.bexio_id,
            'user_id': 1,
            'bank_account_id': 1,
            'currency_id': 1,
            'is_compact_view': True,
            'is_valid_from': '2017-11-09',
            'is_valid_to': '2017-11-09',
            'language_id': 1,
            'logopaper_id': 1,
            'mwst_is_net': True,
            'mwst_type': 0,
            'nb_decimals_amount': 2,
            'nb_decimals_price': 2,
            'payment_type_id': 1,
            'show_position_taxes': False,
            # optional
            'footer': 'Bitte überweisen!',
            'header': 'hey du!',
        }

        # this makes up the total amount
        invoice_data.update({
            'positions': [
                {
                    'type': "KbPositionArticle",
                    'article_id': 1,
                    'unit_price': 1500,
                    'amount': 1,
                    'tax_id': 3
                }
            ]
        })

        # create invoice in bexio
        invoice = self.bexio_api.invoices.update_or_create(
            oid=self.bexio_id, **invoice_data)

        # assign bexio id to Invoice instance
        if not self.bexio_id:
            self.bexio_id = invoice.json().get('id')
            self.save()

        # elif self.captured_amount > 0:
        #     api.invoices.make_payment(
        #         self.bexio_id, float(self.captured_amount))

        return invoice

    class Meta:
        abstract = True
