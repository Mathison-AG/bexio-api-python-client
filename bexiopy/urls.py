# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'auth/$',
        views.BexioAuthentication.as_view(),
        name='authenticate'),

    url(r'', views.HomePage.as_view()),
]
