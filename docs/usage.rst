=====
Usage
=====

To use Bexio API Python Client in a project, add it to your `INSTALLED_APPS`:

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
