# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, you can obtain one at http://mozilla.org/MPL/2.0/.
import requests
import json
import logging
import os

from redash.models import Query
from redash.handlers.base import BaseResource, get_object_or_404
from redash.permissions import require_permission

from redash_stmo import settings
from redash_stmo.resources import add_resource


logger = logging.getLogger(__name__)


class IodidePostResource(BaseResource):
    @require_permission("view_query")
    def get(self, query_id):
        query = get_object_or_404(
            Query.get_by_id,
            query_id,
        )
        url = "https://stage.iodide.nonprod.dataops.mozgcp.net/api/v1/notebooks/"
        template = open(
            "/extension/src/redash_stmo/integrations/iodide/iodide-template.iomd",
            "r"
        )
        completed_template = template.read().replace(
            "[QUERY_ID]",
            query_id
        ).replace(
            "[REDASH_API_KEY]",
            settings.REDASH_OWN_API_KEY_FOR_IODIDE
        ).replace(
            "[TITLE]",
            query.name
        )
        headers = {
            "Authorization": "Token %s" % settings.IODIDE_API_KEY,
        }
        data = {
            "owner": "jkarahalis@mozilla.com",
            "title": query.name,
            "content": completed_template,
        }
        template.close()
        result = requests.post(url, headers=headers, data=data)
        return json.loads(result.content)


def extension(app=None):
    logger.info("Loading Iodide integration extension")
    add_resource(
        app,
        IodidePostResource,
        "/api/integrations/iodide/<query_id>/create"
    )
    logger.info("Loaded Iodide integration extension")
