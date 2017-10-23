=============================
Bexio API Python Client
=============================

.. image:: https://badge.fury.io/py/bexio-api-python-client.svg
    :target: https://badge.fury.io/py/bexio-api-python-client

.. image:: https://travis-ci.org/oesah/bexio-api-python-client.svg?branch=master
    :target: https://travis-ci.org/oesah/bexio-api-python-client

.. image:: https://codecov.io/gh/oesah/bexio-api-python-client/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/oesah/bexio-api-python-client

Bexio API Python Client

Documentation
-------------

The full documentation is at https://bexio-api-python-client.readthedocs.io.

Quickstart
----------

Install Bexio API Python Client::

    pip install bexio-api-python-client

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'bexiopy.apps.BexiopyConfig',
        ...
    )

Add Bexio API Python Client's URL patterns:

.. code-block:: python

    from bexiopy import urls as bexiopy_urls


    urlpatterns = [
        ...
        url(r'^', include(bexiopy_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
