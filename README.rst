=============================
Django flexible parameters
=============================

.. image:: https://badge.fury.io/py/django-flexible-parameters.svg
    :target: https://badge.fury.io/py/django-flexible-parameters

.. image:: https://travis-ci.org/PetrDlouhy/django-flexible-parameters.svg?branch=master
    :target: https://travis-ci.org/PetrDlouhy/django-flexible-parameters

.. image:: https://codecov.io/gh/PetrDlouhy/django-flexible-parameters/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/PetrDlouhy/django-flexible-parameters

Add flexible parameters to your models. Parameters can be defined in admin including their data type. Then you can add various parameters to the base model.

NOTE: This is in early stage of development. Anything can be broken. The mechanism for connecting parameters to your models will need to be rearranged.

Documentation
-------------

The full documentation is at https://django-flexible-parameters.readthedocs.io.

Quickstart
----------

Install Django flexible parameters::

    pip install django-flexible-parameters

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'flexible_parameters.apps.FlexibleParametersConfig',
        ...
    )

Override `BaseParameter` and all other `*Parameter` classers with your own foreign key:

.. code-block:: python

   class AssetParameter(BaseParameter):
       asset = models.ForeignKey(
           "assets.Asset",
           on_delete=models.CASCADE,
       )
   

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
