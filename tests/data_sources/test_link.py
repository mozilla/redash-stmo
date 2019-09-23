from tests import BaseTestCase
from redash_stmo.data_sources.link.extension import DATASOURCE_URLS


class TestDatasourceLink(BaseTestCase):
    def test_gets_datasource_link_and_type(self):
        admin = self.factory.create_admin()
        data_source = self.factory.create_data_source()

        rv = self.make_request(
            "get", "/api/data_sources/{}/link".format(data_source.id), user=admin
        )
        self.assertEqual(200, rv.status_code)
        self.assertEqual(
            rv.json["message"]["type_name"], data_source.query_runner.name()
        )
        self.assertEqual(rv.json["message"]["doc_url"], DATASOURCE_URLS["pg"])
