import json
import os
import mock

from tests import BaseTestCase

from mock import patch
from six.moves import reload_module
from redash_stmo import settings


class TestIodideIntegration(BaseTestCase):
    SETTING_OVERRIDES = {"REDASH_IODIDE_URL": "https://example.com/"}

    def setUp(self):
        super(TestIodideIntegration, self).setUp()
        variables = self.SETTING_OVERRIDES.copy()
        with patch.dict(os.environ, variables):
            reload_module(settings)

        # Queue a cleanup routine that reloads the settings without overrides
        # once the test ends
        self.addCleanup(lambda: reload_module(settings))

    def test_settings(self):
        admin = self.factory.create_admin()

        rv = self.make_request("get", "/api/integrations/iodide/settings", user=admin)
        self.assertEquals(rv.status_code, 200)
        self.assertEquals(
            rv.json, {"iodideURL": self.SETTING_OVERRIDES["REDASH_IODIDE_URL"]}
        )

    @mock.patch("requests.post")
    def test_notebook_post(self, mock_post):
        admin = self.factory.create_admin()
        data_source = self.factory.create_data_source()
        query = self.factory.create_query(
            user=admin, data_source=data_source, query_text="select * from events"
        )

        mock_value = {"id": query.id}
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.text = json.dumps(mock_value)
        mock_json = mock.Mock()
        mock_json.return_value = mock_value
        mock_response.json = mock_json
        mock_post.return_value = mock_response

        rv = self.make_request(
            "post", "/api/integrations/iodide/%s/notebook" % query.id, user=admin
        )
        self.assertEquals(rv.status_code, 200)
        self.assertEquals(rv.json, {"id": query.id})
