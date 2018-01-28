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

    class Meta:
        abstract = True
