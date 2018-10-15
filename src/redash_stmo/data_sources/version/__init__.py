import json
import logging

from redash_stmo.resources import add_resource

from redash.models import DataSource
from redash.handlers.base import BaseResource, get_object_or_404
from redash.permissions import require_access, view_only

logger = logging.getLogger(__name__)


DATASOURCE_VERSION_PARSE_INFO = {
    "pg": {
        "version_query": "select version()",
        "delimiter": " ",
        "index": 1
    },
    "redshift": {
        "version_query": "select version()",
        "delimiter": " ",
        "index": -1
    },
    "mysql": {
        "version_query": "select version()",
        "delimiter": "-",
        "index": 0
    }
}

class DataSourceVersionResource(BaseResource):
    def get(self, data_source_id):
        data_source = get_object_or_404(
            DataSource.get_by_id_and_org,
            data_source_id,
            self.current_org
        )
        require_access(data_source.groups, self.current_user, view_only)
        version_info = get_data_source_version(data_source.query_runner)
        return {"version": version_info}

def get_data_source_version(query_runner):
    parse_info = DATASOURCE_VERSION_PARSE_INFO.get(query_runner.type())
    if parse_info is None:
        return None

    data, error = query_runner.run_query(parse_info["version_query"], None)
    if error is not None:
        logger.error(
            "Unable to run version query for %s: %s", query_runner.type(), error)
        return None
    try:
        version = json.loads(data)['rows'][0]['version']
    except (KeyError, IndexError) as err:
        logger.exception(
            "Unable to parse data source version for %s: %s", query_runner.type(), err)
        return None

    version = version.split(parse_info["delimiter"])[parse_info["index"]]
    return version

def version(app=None):
    add_resource(app, DataSourceVersionResource, '/api/data_sources/<data_source_id>/version')
