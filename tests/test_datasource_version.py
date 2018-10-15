import json
import mock

from tests import BaseTestCase
from flask import Flask

from redash.models import DataSource
from redash.query_runner.pg import PostgreSQL
from redash_stmo.data_sources.version import version


class TestDatasourceVersion(BaseTestCase):
    EXPECTED_DOC_URL = "www.example.com"
    def setUp(self):
        super(TestDatasourceVersion, self).setUp()
        self.admin = self.factory.create_admin()
        self.data_source = self.factory.create_data_source()
        self.patched_run_query = self._setup_mock('redash.query_runner.pg.PostgreSQL.run_query')
        self.patched_runner_type = self._setup_mock('redash.query_runner.pg.PostgreSQL.type')
        version(self.app)

    def _setup_mock(self, function_to_patch):
        patcher = mock.patch(function_to_patch)
        patched_function = patcher.start()
        self.addCleanup(patcher.stop)
        return patched_function

    def _test_expected_version_returned(self, expected_version, version_string, runner_type):
        self.patched_runner_type.return_value = runner_type
        self.patched_run_query.return_value = (json.dumps({
            "rows":
                [{ "version": version_string.format(version=expected_version) }]
        }), None)
        rv = self.make_request('get', '/api/data_sources/{}/version'.format(self.data_source.id), user=self.admin)
        self.assertEqual(200, rv.status_code)
        self.assertEqual(rv.json['version'], expected_version)

    def test_gets_postgres_version(self):
        RUNNER_TYPE = "pg"
        DATASOURCE_VERSION = "9.5.10"
        VERSION_STRING = (
            "PostgreSQL {version} on x86_64-pc-linux-gnu, compiled by gcc "
            "(GCC) 4.8.3 20140911 (Red Hat 4.8.3-9), 64-bit"
        )
        self._test_expected_version_returned(DATASOURCE_VERSION, VERSION_STRING, RUNNER_TYPE)

    def test_gets_redshift_version(self):
        RUNNER_TYPE = "redshift"
        DATASOURCE_VERSION = "1.0.3688"
        VERSION_STRING = (
            "PostgreSQL 8.0.2 on i686-pc-linux-gnu, compiled by GCC "
            "gcc (GCC) 3.4.2 20041017 (Red Hat 3.4.2-6.fc3), Redshift {version}"
        )
        self._test_expected_version_returned(DATASOURCE_VERSION, VERSION_STRING, RUNNER_TYPE)

    def test_gets_mysql_version(self):
        RUNNER_TYPE = "mysql"
        DATASOURCE_VERSION = "5.7.16"
        VERSION_STRING = "{version}-log"
        self._test_expected_version_returned(DATASOURCE_VERSION, VERSION_STRING, RUNNER_TYPE)

    def test_unexpected_json(self):
        self.patched_runner_type.return_value = "pg"
        self.patched_run_query.return_value = (json.dumps({
            "rows":
                [{ "bad_json": "foo" }]
        }), None)
        rv = self.make_request('get', '/api/data_sources/{}/version'.format(self.data_source.id), user=self.admin)
        self.assertEqual(200, rv.status_code)
        self.assertEqual(rv.json['version'], None)
