# -*- coding: utf-8 -*-
from django.db import models


class BexioSession(models.Model):

    code = models.CharField(
        max_length=255,
        verbose_name='code',
        null=True, blank=True)

    access_token = models.CharField(
        max_length=255,
        verbose_name='access token',
        null=True, blank=True)

    expires_in = models.IntegerField(
        verbose_name='expires in (seconds)',
        null=True, blank=True)

    token_type = models.CharField(
        max_length=255,
        verbose_name='token type',
        default='Bearer')

    scope = models.CharField(
        max_length=255,
        verbose_name='scope',
        null=True, blank=True)

    refresh_token = models.CharField(
        max_length=255,
        verbose_name='refresh token',
        null=True, blank=True)

    org = models.CharField(
        max_length=255,
        verbose_name='organization',
        null=True, blank=True)

    user_id = models.IntegerField(
        verbose_name='user id',
        null=True, blank=True)
