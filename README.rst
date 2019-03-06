Redash-STMO
===========

`Redash <https://redash.io>`_ extensions for
`sql.telemetry.mozilla.org <https://sql.telemetry.mozilla.org/>`_.

Or as it should have been called: *St. Moredash* ;)

.. image:: https://circleci.com/gh/mozilla/redash-stmo.svg?style=svg
    :target: https://circleci.com/gh/mozilla/redash-stmo

.. image:: https://codecov.io/gh/mozilla/redash-stmo/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/mozilla/redash-stmo

.. image:: https://img.shields.io/badge/calver-YY.M.PATCH-22bfda.svg
   :target: https://calver.org/
   :alt: CalVer - Timely Software Versioning

Installation
------------

Please install the package using your favorite package installer::

    pip install redash-stmo

Development
-----------

Running the full site please run:

```
make up
```

To also run the webpack devserver please run in parallel:

```
make devserver
```

To enter the container and run a bash shell run:

```
make bash
```

To run the tests (from the host machine) run:

```
make test
```

Issues & questions
------------------

See the `issue tracker on GitHub <https://github.com/mozilla/redash-stmo/issues>`_
to open tickets if you have issues or questions about Redash-STMO.
