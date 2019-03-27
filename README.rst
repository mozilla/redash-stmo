Redash-STMO
===========

`Redash <https://redash.io>`_ extensions for
`sql.telemetry.mozilla.org <https://sql.telemetry.mozilla.org/>`_.

Or as it should have been called: *St. Moredash* ;)

.. image:: https://circleci.com/gh/mozilla/redash-stmo.svg?style=svg
    :target: https://circleci.com/gh/mozilla/redash-stmo

.. image:: https://codecov.io/gh/mozilla/redash-stmo/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/mozilla/redash-stmo

.. image:: https://img.shields.io/badge/calver-YYYY.M.PATCH-22bfda.svg
   :target: https://calver.org/
   :alt: CalVer - Timely Software Versioning

Installation
------------

Please install the package using your favorite package installer::

    pip install redash-stmo

Development
-----------

During the development we're providing some convenience Make tasks that are
supposed to be run from the Docker host machine, not from inside a container.

Create the database
~~~~~~~~~~~~~~~~~~~

Only once please::

    make database

Install NPM modules
~~~~~~~~~~~~~~~~~~~

First install the Node modules::

    make node_modules

Start the containers
~~~~~~~~~~~~~~~~~~~~

Start backend, Celery, Redis, Postgres::

    make up

Run webpack devserver
~~~~~~~~~~~~~~~~~~~~~

Please run in parallel to the containers above::

    make devserver

Start shell
~~~~~~~~~~~

To enter the container and run a bash shell run::

    make bash

Run tests
~~~~~~~~~

To run the tests (from the host machine) run::

    make test

Issues & questions
------------------

See the `issue tracker on GitHub <https://github.com/mozilla/redash-stmo/issues>`_
to open tickets if you have issues or questions about Redash-STMO.
