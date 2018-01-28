=============================
Bexio API Python Client
=============================

.. image:: https://badge.fury.io/py/bexio-api-python-client.svg
    :target: https://badge.fury.io/py/bexio-api-python-client

.. image:: https://travis-ci.org/oesah/bexio-api-python-client.svg?branch=master
    :target: https://travis-ci.org/oesah/bexio-api-python-client

.. image:: https://codecov.io/gh/oesah/bexio-api-python-client/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/oesah/bexio-api-python-client

.. image:: https://api.codeclimate.com/v1/badges/a3b970ccfc691d06c052/maintainability
   :target: https://codeclimate.com/github/oesah/bexio-api-python-client/maintainability
   :alt: Maintainability


Bexio API Python Client. It works as a standalone lib in python, but needs
additional work to get it started. There is a Django integration, that works
out of the box, once you set it up properly as described later. If you wish to 
use it with Python alone, you can take a look at the Django integration. It
shows how you can use it with python alone.

Features
--------

* API connection to your Bexio instance
* Django integration
* Creation & Auto-renewal of access token

Documentation
-------------

The full documentation is at https://bexio-api-python-client.readthedocs.io.

Quickstart
----------

Install Bexio API Python Client::

    pip install bexio-api-python-client

If you are using anything other than Django with this module, you need to
write some more code to authenticate and use the API. Check out the Django
parts of the module to see how it can be done.

Django Integration
------------------

You can use the API directly with Django. There are URLs, Views and other
helpers to integrate the API into your Django project.

Add it to your :code:`INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'bexiopy.apps.BexiopyConfig',
        ...
    )

Add Bexio API Python Client's URL patterns to your main :code:`urls.py`:

.. code-block:: python

    from bexiopy import urls as bexiopy_urls


    urlpatterns = [
        ...
        url(r'bexiopy/', include('bexiopy.urls', namespace='bexiopy')),
        ...
    ]


Docker
------

If you use docker, you can configure a volume to store the token:

Example:

.. code-block:: yaml
    
    # docker-compose.yml
    volumes:
        bexio_token: {}

    services:
        app:
            volumes:
                - bexio_token:/app/secrets

    # app/Dockerfile
    ...
    RUN mkdir /app/secrets
    ...


Basic Usage
-----------

See docs for basic usage: https://bexio-api-python-client.readthedocs.io/en/latest/bexiopy.html#bexiopy.api.Client

You can also use helper functions, so you don't need to create the :code:`call` every time (see docs).
These helper functions are added over time, but you can use the API fully, with the
`call` function. The helper methods only offer nicer ways to query the API (e.g. :code:`Bexiopy().contacts.get(2)`).
The progress of the helper functions are documented below under "Progress".


Settings
--------

Configure the minimum :code:`settings.py` (check docs for all options):

.. code-block:: python

    BEXIO_CLIENT_SECRET = 'my_secret'
    BEXIO_CLIENT_ID = 'my_id'
    BEXIO_APPLICATION_SCOPES = ['my_scope_1', 'my_scope_2']
    BEXIO_APPLICATION_REDIRECTION_URL = 'https://example.com'


Start the server and go to :code:`/bexiopy/auth/` and authenticate with Bexio.

**i18n URLs**

If you have internationalized URLs, then make sure you place the Bexiopy
url outside the internationalized ones, so it can be called without any
language code (:code:`/bexiopy/auth/` instead of :code:`/en/bexiopy/auth/`).


Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools and libs used in creating this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_
*  `Christian Ruhstaller (bexio-api-php-client)`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
.. _`Christian Ruhstaller (bexio-api-php-client)`: https://github.com/christianruhstaller/bexio-api-php-client


Progress
--------
[ ] = Open

[~] = In Progress

[X] = Done

[-] = Not possible / Ignored



Contacts
^^^^^^^^

Contacts
========

* [X] List contacts
* [X] Search contacts
* [X] Show contact
* [X] Create contact
* [X] Overwrite contact
* [X] Edit contact
* [X] Delete contact
* [ ] Bulk create contact


Salutations
===========

* [ ] List salutations
* [ ] Search salutations
* [ ] Show salutation
* [ ] Create salutation
* [ ] Overwrite salutation
* [ ] Edit salutation
* [ ] Delete salutation


Titles
======

* [ ] List titles
* [ ] Search titles
* [ ] Show title
* [ ] Create title
* [ ] Overwrite title
* [ ] Edit title
* [ ] Delete title


Invoices
^^^^^^^^
* [X] List invoices 
* [X] Search invoices 
* [X] Show invoice 
* [X] Create invoice 
* [X] Overwrite invoice 
* [X] Edit invoice 
* [X] Delete invoice 
* [X] Show invoice pdf 
* [X] Copy invoice 
* [ ] Issue invoice 
* [ ] Mark invoice as sent 
* [ ] Send invoice 
* [ ] List comments 
* [ ] Search comments 
* [ ] Show comment 
* [ ] Create comment 
* [-] List payments 
* [-] Show payments 
* [-] Create payments 
* [-] Delete payments 
