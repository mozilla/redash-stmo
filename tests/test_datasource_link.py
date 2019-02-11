import mock

from tests import BaseTestCase


class TestDatasourceLink(BaseTestCase):
    EXPECTED_DOC_URL = "www.example.com"

    def setUp(self):
        super(TestDatasourceLink, self).setUp()
        self.patched_query_runners = self._setup_mock('redash_stmo.data_sources.link.query_runners')
        self.patched_query_runners.return_value = {}

    def _setup_mock(self, function_to_patch):
        patcher = mock.patch(function_to_patch)
        patched_function = patcher.start()
        self.addCleanup(patcher.stop)
        return patched_function

    def test_gets_datasource_link_and_type(self):
        admin = self.factory.create_admin()
        data_source = self.factory.create_data_source()
        data_source.options["doc_url"] = self.EXPECTED_DOC_URL

        rv = self.make_request('get', '/api/data_sources/{}/link'.format(data_source.id), user=admin)
        self.assertEqual(200, rv.status_code)
        self.assertEqual(rv.json['message']['type_name'], data_source.query_runner.name())
        self.assertEqual(rv.json['message']["doc_url"], self.EXPECTED_DOC_URL)
