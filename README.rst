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

Overview
--------

Inherits Redash's Docker setup
  redash-stmo is using Redash's own Docker image for development to implement a
  close development/production parity and extends it in various ways, e.g.
  an own docker-compose configuration, an own docker-entrypoint script.

  Specifically it uses Mozilla's "rc" tagged version of the Redash Docker
  image, which includes (at the time of writing this, 2019-06-13) many
  customizations from Mozilla's pseudo-temporary and regularly updated Redash
  fork. The "rc" tagged Docker image is updated every time a "rebase" from
  upstream Redash happens and is put to testing in the "release" Redash
  environment on Mozilla's server.

  Please review the `Redash Docker installation guidelines <https://redash.io/help/open-source/dev-guide/docker>`_ before continuing. It's important to know
  those basics since many decisions for redash-stmo were derived from it.
  Thank you.

Is mounted under /extension
  The current working directory (the directory with this ``README.rst``) is
  mounted under the path ``/extension`` by docker-compose inside the Docker
  container.

Runs with Redash in /app
  Since it reuses the Redash Docker image, you can find all the Redash setup
  under the ``/app`` directory inside the Docker container.

Uses Redash's "entrypoints" for discovery
  The way Redash finds new extensions is by using the so called "entrypoints"
  of Python packages, metadata that is specified and distributed in
  Python packages, that is read out by Redash at runtime to find the filesystem
  locations for Redash extensions.

  That's true for three kinds of entrypoints:

  ``redash.extensions``
    Python callables to be used to extend the Redash Flask app, e.g.
    ``redash_stmo.data_sources.health:extension``.

  ``redash.bundles``
    Python packages that contain additional front-end files for the
    webpack build process, e.g. ``redash_stmo.data_sources.link``.

  ``redash.periodic_tasks``
    Python callables that return parameters for periodic Celery tasks,
    e.g. ``redash_stmo.data_sources.health:periodic_task``.

Hooks into Webpack
  Since Redash extensions like redash-stmo can also provide additional Webpack
  bundles, the development setup runs Redash's `bundle-extension script <https://github.com/getredash/redash/blob/master/bin/bundle-extensions>`_ periodically
  to copy the files from redash-stmo to the right place for webpack to pick
  them up (``/app/client/app/extensions``).

  See the section about the webpack development server below for more
  information.

Development workflow
--------------------

We provide some convenience Make tasks to be run from your host machine
(not inside the Docker container) to ease this non-trivial application setup:

Build and update the local Docker image
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Many of the helpers below will implicitely run docker-compose to start the
Redash containers and in effect automatically build the local Docker image
as well if it doesn't exist.

If you'd like to build the local Docker image separately or if you'd like to
fetch the latest version of the base Redash Docker image (or its child
image of the Mozilla Redash fork), e.g. in the event of a new rebase by
Mozilla staff, please run the following::

    make build

Behind the scenes
   This will run ``docker-compose build --pull`` which will pull updates to
   the Docker images used by the docker-compose setup, including the Redash,
   Redis and Postgres images.

Create the database
~~~~~~~~~~~~~~~~~~~

On you command line run this **ONCE** to create the database for
Redash/redash-stmo setup:

::

    make database

This uses Redash's own ability and redash-stmo is just set up to reuse it.

Behind the scenes
  This will run docker-compose to create the server container that is
  running the Redash Python server and in effect the Redis and Postgres
  containers, too.

  It will then initialize the Postgres tables needed for Redash.

Install npm modules
~~~~~~~~~~~~~~~~~~~

Then we'll install the Redash npm modules inside the server container::

    make node_modules

Behind the scenes
  This will run ``npm install`` inside the server in the ``/app`` directory,
  which is the directory with Redash's code from the Redash Docker base
  image.

  NOTE, the redash-stmo development setup mounts the ``/app/node_modules``
  directory as a separate Docker volume, that will be maintained by Docker
  and won't show up in or transfer to the host machine where Docker is
  running.

Start the containers
~~~~~~~~~~~~~~~~~~~~

To start the whole set of Docker containers for a working environment
(Redash server, Celery workers, Redis, Postgres) all you need to run is this::

    make up

Behind the scenes
  This is pretty simply running ``docker-compose up``, to launch all
  containers of the redash-stmo Docker setup.

  NOTE: This **requires** first installing npm modules inside the container
  above and creating the database as well!

Run webpack devserver
~~~~~~~~~~~~~~~~~~~~~

If you're developing a Redash extension that includes an additional webpack
bundle (which will need to be included in Redash's webpack build process
to be shipped in the client application bundle) you'll want to use the webpack
development server.

It automatically compiles the Redash client application bundle on files
changes and proxies requests for the Redash server via a proxy running
on port 8080 (instead of the usual Redash port of 5000).

After starting the containers using the description in the above step,
open a second terminal and **additionally run**::

    make devserver

Behind the scenes
  This will run the webpack devserver in another instance of the server
  container (not the same as when running ``make up``) and runs a script
  that listens for files changes to ``.js`` and ``.jsx`` files in the
  ``/extension`` directory.

  When changes are detected, it'll automatically run Redash's
  ``bundle-extensions`` script that does the heavy lifting of copying
  the changed extension files into the ``/app/client/app/extensions``
  directory, which triggers the webpack devserver to recompile the
  client application bundle.

  NOTE: This **requires** opening the Redash instance via
  http://localhost:8080/ instead of http://localhost:5000/ to go through
  the webpack devserver.


Start shell
~~~~~~~~~~~

In case you need to do any debugging or file system checks inside the
server container, you can create a bash shell by running::

    make bash

Behind the scenes
  Any changes you make here outside the ``/extension`` directory
  (which is mounted as a Docker volume with the current working directory on
  the Docker host machine) and the following directores are not persisted.

  List of directories inside the container that are mounted as Docker volumes:

  ``/extension``
    Maps the current working directory (where this README.rst is located)
    on the host machine for developing the extension.

  ``/home/redash/.cache``
    Used by pip and other scripts,

  ``/app/client/dist``
    Directory to retain webpack build results, so webpack builds don't take
    as long on consecutive runs.

  ``/home/redash/.local``
    Directory for "user-installed" Python packages. If you'd like you can
    easily install additonal Python packages with the Docker container user
    Redash using ``pip install --user <package>``. Installed scripts from
    those packages will be found under ``/home/redash/.local/bin`` but
    are also automatically added to ``PATH``.

  ``/app/node_modules``
    Directory for npm modules, that are installed when running ``npm install``
    inside of ``/app`` in the container. Retained to make use of native npm
    caching between consecutive runs.

Run tests
~~~~~~~~~

Running the Python based tests requires first creating a separate database
(implemented by the ``test_database`` Make task) and then running the test
runner inside the container. The test database is not the same as the
databse in use for regular development (e.g. to not overwrite development
data).

Frontend or integration tests are currently not supported.

To run the tests (from the host machine) run::

    make test

This will automatically run the ``test_database`` Make task before running
the tests.

Behind the scenes
  When launching the tests runner it'll the regular server container,
  but also set the ``REDASH_DATABASE_URL`` environment variable to the
  test database to prevent overwriting any data that you added to the
  database the regular Redash interface (e.g. data sources, queries etc).

  By default it uses `pytest <https://docs.pytest.org/>`_ to run
  the Python tests in ``/extension``, with a number of parameters as
  defined in the ``pytest.ini``.

  If you'd like to add additional parameters to pytest simply appened the
  command line arguments in ``pytest.ini``.

  Alternatively, e.g. if you'd like to use `pdb <https://docs.python.org/3/library/pdb.html>`_ to debug a test, do this:

  create the test database from the host machine
    ``make test_database``

  start a Bash shell in the container
    ``make bash``

  set the ``REDASH_DATABASE_URL`` env var in the container
    ``export REDASH_DATABASE_URL="postgresql://postgres@postgres/tests"``

  change direcotry to extensio code
    ``cd /extension``

  run the tests with whatever parameter
    ``pytest -vvv --pdb``

Issues & questions
------------------

See the `issue tracker on GitHub <https://github.com/mozilla/redash-stmo/issues>`_
to open tickets if you have issues or questions about Redash-STMO.
