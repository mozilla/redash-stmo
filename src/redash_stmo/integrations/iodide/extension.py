# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, you can obtain one at http://mozilla.org/MPL/2.0/.
import requests
import logging
import os

from flask import render_template_string
from redash.models import Query
from redash.handlers.authentication import base_href
from redash.handlers.base import BaseResource, get_object_or_404
from redash.permissions import require_permission

from redash_stmo import settings
from redash_stmo.resources import add_resource


logger = logging.getLogger(__name__)


class IodideNotebookResource(BaseResource):
    TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'iodide-notebook.iomd.j2')

    @require_permission("view_query")
    def post(self, query_id):
        query = get_object_or_404(
            Query.get_by_id_and_org,
            query_id,
            self.current_org,
        )

        with open(self.TEMPLATE_PATH, "r") as template:
            source = template.read()
            context = {
                "redash_url": base_href(),
                "query_id": query_id,
                "title": query.name,
                "api_key": settings.IODIDE_DEFAULT_API_KEY,
            }
            rendered_template = render_template_string(source, **context)
        headers = {
            "Authorization": "Token %s" % settings.IODIDE_AUTH_TOKEN,
        }
        data = {
            "owner": self.current_user.email,
            "title": query.name,
            "content": rendered_template,
        }
        response = requests.post(settings.IODIDE_NOTEBOOK_API_URL, headers=headers, data=data)
        return response.json()


class IodideSettingsResource(BaseResource):
    @require_permission("view_query")
    def get(self):
        return {
            "iodideURL": settings.IODIDE_URL,
        }


def extension(app=None):
    logger.info("Loading Iodide integration extension")
    add_resource(
        app,
        IodideNotebookResource,
        "/api/integrations/iodide/<query_id>/notebook",
    )
    add_resource(
        app,
        IodideSettingsResource,
        "/api/integrations/iodide/settings",
    )
    logger.info("Loaded Iodide integration extension")
