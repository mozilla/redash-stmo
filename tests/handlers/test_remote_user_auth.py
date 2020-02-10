import mock
from flask import url_for
from redash import settings
from redash.authentication.org_resolving import current_org
from redash_stmo import settings as extension_settings
from tests import BaseTestCase


class TestLogin(BaseTestCase):
    @mock.patch("redash.settings.REMOTE_USER_LOGIN_ENABLED", return_value=True)
    def test_custom_login(self, remote_user_login_enabled_mock):
        """Test to make sure requests to /login are directed to the
        remote auth URL"""
        test_url = "/login"
        with self.app.test_request_context(test_url):
            response = self.client.get(test_url)
            self.assertEqual(response.status_code, 302)
            self.assertEqual(
                response.location,
                url_for(
                    "remote_user_auth.login",
                    next=url_for(
                        "redash.index", org_slug=current_org.slug, _external=False
                    ),
                    org_slug=current_org.slug,
                    _external=True,
                ),
            )


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
        test_url = "/remote_user/login?next=%2F"

        with self.app.test_request_context(test_url):
            # make sure to call the before_request callback used
            self.app.preprocess_request()
            response = self.get_request(
                test_url, headers={"X-Forwarded-Remote-Groups": "staff,contributors"}
            )
            self.assertTrue(mock_logger.called)
            self.assertEqual(response.status_code, 302)
            index_url = url_for("redash.index", next=next_path, _external=True)
            self.assertEqual(response.location, index_url)
