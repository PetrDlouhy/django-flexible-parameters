=====
Usage
=====

To use Django flexible parameters in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'flexible_parameters.apps.FlexibleParametersConfig',
        ...
    )

Add Django flexible parameters's URL patterns:

.. code-block:: python

    from flexible_parameters import urls as flexible_parameters_urls


    urlpatterns = [
        ...
        url(r'^', include(flexible_parameters_urls)),
        ...
    ]
