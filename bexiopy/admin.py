# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import BexioSession


@admin.register(BexioSession)
class BexioSessionAdmin(admin.ModelAdmin):
    pass
