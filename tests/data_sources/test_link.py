import json

from redash_stmo.data_sources.link.extension import DATASOURCE_URLS
from tests import BaseTestCase, authenticate_request


class TestDatasourceLink(BaseTestCase):
    def test_gets_datasource_link_and_type(self):
        admin = self.factory.create_admin()
        data_source = self.factory.create_data_source()

        authenticate_request(self.client, admin)
        rv = self.client.get("/api/data_sources/{}/link".format(data_source.id))
        self.assertEqual(200, rv.status_code)
        rv_json = json.loads(rv.data)
        self.assertEqual(
            rv_json["message"]["type_name"], data_source.query_runner.name()
        )
        self.assertEqual(rv_json["message"]["doc_url"], DATASOURCE_URLS["pg"])
