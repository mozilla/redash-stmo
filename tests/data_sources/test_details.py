import mock
import json

from redash_stmo.data_sources.details.extension import DATASOURCE_URLS
from redash.utils.configuration import ConfigurationContainer
from tests import BaseTestCase, authenticate_request


class TestDataSourceDetails(BaseTestCase):
    EXPECTED_DOC_URL = "www.example.com"

    def setUp(self):
        super(TestDataSourceDetails, self).setUp()
        self.admin = self.factory.create_admin()
        self.data_source = self.factory.create_data_source(
            options=lambda: ConfigurationContainer.from_json(
                json.dumps(
                    dict(
                        user="postgres",
                        password="postgres",
                        host="postgres",
                        dbname="tests",
                    )
                )
            ),
        )
        self.patched_run_query = self._setup_mock(
            "redash.query_runner.pg.PostgreSQL.run_query"
        )
        self.patched_runner_type = self._setup_mock(
            "redash.query_runner.pg.PostgreSQL.type"
        )
        authenticate_request(self.client, self.admin)

    def _setup_mock(self, function_to_patch):
        patcher = mock.patch(function_to_patch)
        patched_function = patcher.start()
        self.addCleanup(patcher.stop)
        return patched_function

    def _test_expected_version_returned(
        self, expected_version, version_string, runner_type
    ):
        self.patched_runner_type.return_value = runner_type
        self.patched_run_query.return_value = (
            json.dumps(
                {"rows": [{"version": version_string.format(version=expected_version)}]}
            ),
            None,
        )
        rv = self.client.get(
            "/api/data_sources/{}/details".format(self.data_source.id),
        )
        self.assertEqual(200, rv.status_code)
        self.assertEqual(json.loads(rv.data)["message"]["version"], expected_version)

    def test_gets_postgres_version(self):
        RUNNER_TYPE = "pg"
        DATASOURCE_VERSION = "9.5.10"
        VERSION_STRING = (
            "PostgreSQL {version} on x86_64-pc-linux-gnu, compiled by gcc "
            "(GCC) 4.8.3 20140911 (Red Hat 4.8.3-9), 64-bit"
        )
        self._test_expected_version_returned(
            DATASOURCE_VERSION, VERSION_STRING, RUNNER_TYPE
        )

    def test_gets_redshift_version(self):
        RUNNER_TYPE = "redshift"
        DATASOURCE_VERSION = "1.0.3688"
        VERSION_STRING = (
            "PostgreSQL 8.0.2 on i686-pc-linux-gnu, compiled by GCC "
            "gcc (GCC) 3.4.2 20041017 (Red Hat 3.4.2-6.fc3), Redshift {version}"
        )
        self._test_expected_version_returned(
            DATASOURCE_VERSION, VERSION_STRING, RUNNER_TYPE
        )

    def test_gets_mysql_version(self):
        RUNNER_TYPE = "mysql"
        DATASOURCE_VERSION = "5.7.16"
        VERSION_STRING = "{version}-log"
        self._test_expected_version_returned(
            DATASOURCE_VERSION, VERSION_STRING, RUNNER_TYPE
        )

    def test_unexpected_json(self):
        self.patched_runner_type.return_value = "pg"
        self.patched_run_query.return_value = (
            json.dumps({"rows": [{"bad_json": "foo"}]}),
            None,
        )
        rv = self.client.get(
            "/api/data_sources/{}/details".format(self.data_source.id),
        )
        self.assertEqual(200, rv.status_code)
        self.assertEqual(json.loads(rv.data)["message"]["version"], None)

    def test_gets_datasource_link_and_type(self):
        self.patched_runner_type.return_value = "pg"
        VERSION_STRING = (
            "PostgreSQL 8.0.2 on i686-pc-linux-gnu, compiled by GCC "
            "gcc (GCC) 3.4.2 20041017 (Red Hat 3.4.2-6.fc3), Redshift {version}"
        )
        self.patched_run_query.return_value = (
            json.dumps({"rows": [{"version": VERSION_STRING}]}),
            None,
        )
        rv = self.client.get("/api/data_sources/{}/details".format(self.data_source.id))
        self.assertEqual(200, rv.status_code)
        rv_json = json.loads(rv.data)
        self.assertEqual(
            rv_json["message"]["type_name"], self.data_source.query_runner.name()
        )
        self.assertEqual(rv_json["message"]["doc_url"], DATASOURCE_URLS["pg"])
