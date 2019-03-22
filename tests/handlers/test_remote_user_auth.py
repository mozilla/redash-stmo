import mock
from flask import url_for
from redash import settings

from redash_stmo import settings as extension_settings
from tests import BaseTestCase


class TestRemoteAuthGroups(BaseTestCase):
    @mock.patch.object(settings, "REMOTE_USER_LOGIN_ENABLED", return_value=True)
    @mock.patch.object(extension_settings, "REMOTE_GROUPS_ENABLED", return_value=True)
    @mock.patch.object(
        extension_settings,
        "REMOTE_GROUPS_ALLOWED",
        return_value=set(["admins", "managers"]),
    )
    @mock.patch("redash.authentication.remote_user_auth.logger.error")
    def test_redirect_if_disabled(self, mock_logger, *args, **kwargs):
        """Test to make sure requests to /login are directed to the
        remote auth URL"""
        next_path = "/"
        if settings.MULTI_ORG:
            test_url = url_for(
                "remote_user_auth.login", org_slug="default", next=next_path
            )
        else:
            test_url = url_for("remote_user_auth.login", next=next_path)

        with self.app.test_request_context(test_url):
            # make sure to call the before_request callback used
            self.app.preprocess_request()
            response = self.get_request(
                test_url, headers={"X-Forwarded-Remote-Groups": "staff,contributors"}
            )
            self.assertTrue(mock_logger.called)
            self.assertEqual(response.status_code, 302)
            index_url = url_for(
                "redash.index", org_slug="default", next=next_path, _external=True
            )
            self.assertEqual(response.location, index_url)
