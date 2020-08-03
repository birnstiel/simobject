.. image:: https://codecov.io/gh/birnstiel/simobject/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/birnstiel/simobject

.. image:: https://travis-ci.org/birnstiel/simobject.svg?branch=master
  :target: https://travis-ci.org/birnstiel/simobject

.. image:: https://readthedocs.org/projects/simobject/badge/?version=latest
  :target: https://simobject.readthedocs.io/en/latest/?badge=latest
  :alt: Documentation Status


Readme
======

General framework for a simulation:

- `Simulation` object with `Quantities` that can be updated in a specified order
- `Quantities` objects that behave like `numpy.ndarrays` but can be set to be constant, contain information, and have functions to update them.
- `Updater` object that can define how a quantity is updated.
- `Simulation` and `Quantities` inherit from the `HeartbeatObject` which provide a `Systoler`, `Updater`, and `Diastoler` (those are also all `Updater` objects) and functions to call or set them
- The `Simulation` object has its own update function which in this order
  - calls its own `systole` update
  - calls the `systole` updates of its quantities
  - calls the `update` updates of its quantities
  - calls the `diastole` updates of its quantities
  - calls its own `diastole` update
