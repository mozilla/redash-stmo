Changelog
=========

2019.8.0
--------

:date: 2019-08-13

* Add a custom BigQuery query runner to add labels for better accounting.

* Automatically redirect requests for /login to /remote_user/login.

* Improve BigQuery validation errors.

2019.7.4
--------

:date: 2019-07-17

* Use the correct API key to fetch query result JSON from Iodide

2019.7.3
--------

:date: 2019-07-16

* Fix bug where the "Explore in Iodide" button creates unusable notebooks if
  clicked on Redash staging
* Fix bug where the "Explore in Iodide" button is shown, but non-functional, for
  queries that have never been saved

2019.7.2
--------

:date: 2019-07-11

* Inlcude Jinja templates in Python packages


2019.6.2
--------

:date: 2019-07-08

* Add Iodide integration extension, which adds an "Explore in Iodide" button on
  query pages

2019.6.1
--------

:date: 2019-06-13

* Fix package layout issues with regard to new extension API.

* Various fixes to development workflow.

2019.6.0
--------

:date: 2019-06-12

* Use improved extension layout from upstream, splitting extensions into Python
  extensions, webpack bundles and periodic Celery tasks.

2019.5.0
--------

:date: 2019-05-27

* Fix tiny webpack error.

* Add Mozilla's Community Participation Guidelines as the Code of Conduct.

2019.3.2
--------

:date: 2019-04-02

(this version should have been 2019.4.0 but was accidentally versioned)

* Use lists instead of generator in Presto query runner.

2019.3.1
--------

:date: 2019-03-27

* Reverted PyAthena version pinning again.

2019.3.0
--------

:date: 2019-03-27

* Refactoring some of the tests.

* Add query validation for Postgres and Bigquery data sources.

* Port REMOTE_GROUPS feature from Redash fork.

2019.2.2
--------

:date: 2019-02-28

* New tag line: St. Moredash. (S.T.M.O.R.E.D.A.S.H.)

* Implement own Presto query runner that pretty prints response data.

* Add own query result API endpoint handler that adds aditional permission
  checks for query results that are being referred in a query result based
  query.

* Use mozilla/redash Docker image as base image for tests for improved
  test coverage.

* Move to Circle CI for continuous integration:

    https://circleci.com/gh/mozilla/redash-stmo

2019.2.1
--------

:date: 2019-02-04

* Fix test setup and enabled coverage reporting on codecov:

    https://codecov.io/gh/mozilla/redash-stmo

* Push README to PyPI.

2019.2.0
--------

:date: 2019-02-04

* Fix ESlint errors.

2018.12.0
---------

:date: 2018-12-17

* Fix initialization of datasource frontend extensions.


2018.11.0
---------

:date: 2018-11-27

* Add datasource health API endpoint.

* Reorganizations for data source extensions.

2018.9.1
--------

:date: 2018-09-14

* Add datasource version extension.

* Minor cleanups for datasource link extension.

2018.9.0
--------

:date: 2018-09-11

* Add datasource link extension.

2018.8.1
--------

:date: 2018-08-10

* Fix name of task parameter name.

2018.8.0
--------

:date: 2018-08-09

* Add docker integration for running tests
* Add travis CI integration
* Add datasource health extension and tests

2018.4.0
--------

:date: 2018-04-03

Updated python-dockerflow to 2018.4.0 to fix a
backward-compatibility issue with a dependency.

2018.3.0
--------

:date: 2018-03-08

Copy ActiveData query runner from our Redash fork. Originally written
by Kyle Lahnakoski at https://github.com/klahnakoski/ActiveData-redash-query-runner.

2018.2.3
--------

:date: 2018-02-28

First release that provides automatic support for Dockerflow_.

.._Dockerflow: http://python-dockerflow.readthedocs.io/
