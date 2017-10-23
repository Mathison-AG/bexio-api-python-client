# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url, include

from bexiopy.urls import urlpatterns as bexiopy_urls

urlpatterns = [
    url(r'^', include(bexiopy_urls, namespace='bexiopy')),
]
