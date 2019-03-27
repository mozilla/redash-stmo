from flask import redirect, request, url_for
from redash import settings
from redash.authentication import get_next_path
from redash.authentication.org_resolving import current_org
from redash.authentication.remote_user_auth import logger

from redash_stmo import settings as extension_settings


def check_remote_groups():
    """Check if there is a header of user groups and if yes
    check it against a list of allowed user groups from the settings"""
    # Quick shortcut out if remote user auth or remote groups aren't enabled
    if (
        not settings.REMOTE_USER_LOGIN_ENABLED
        or not extension_settings.REMOTE_GROUPS_ENABLED
    ):
        return

    # Generate the URL to the remote auth login endpoint
    if settings.MULTI_ORG:
        org = current_org._get_current_object()
        remote_auth_path = url_for("remote_user_auth.login", org_slug=org.slug)
    else:
        remote_auth_path = url_for("remote_user_auth.login")

    # Then only act if the request is for the remote user auth view
    if request.path.startswith(remote_auth_path):
        remote_groups = settings.set_from_string(
            request.headers.get(extension_settings.REMOTE_GROUPS_HEADER) or ""
        )
        # Finally check if the remote groups found in the request header
        # intersect with the allowed remote groups
        if not extension_settings.REMOTE_GROUPS_ALLOWED.intersection(remote_groups):
            logger.error(
                "User groups provided in the %s header are not "
                "matching the allowed groups.",
                extension_settings.REMOTE_GROUPS_HEADER,
            )
            # Otherwise redirect back to the frontpage
            unsafe_next_path = request.args.get("next")
            next_path = get_next_path(unsafe_next_path)
            if settings.MULTI_ORG:
                org = current_org._get_current_object()
                index_url = url_for("redash.index", org_slug=org.slug, next=next_path)
            else:
                index_url = url_for("redash.index", next=next_path)
            return redirect(index_url)


def extension(app):
    """An extension that checks the REMOTE_GROUPS_HEADER."""
    app.before_request(check_remote_groups)
