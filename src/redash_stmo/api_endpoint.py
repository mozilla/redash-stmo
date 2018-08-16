import json
from redash import models
from redash.handlers import api
from redash.handlers.base import BaseResource, get_object_or_404
from redash.permissions import require_access, view_only
from redash.query_runner import BaseQueryRunner
from redash.query_runner.pg import PostgreSQL


class DataSourceVersionResource(BaseResource):
    def get(self, data_source_id):
        data_source = get_object_or_404(models.DataSource.get_by_id_and_org, data_source_id, self.current_org)
        require_access(data_source.groups, self.current_user, view_only)
        try:
            version_info = data_source.query_runner.get_data_source_version()
        except Exception as e:
            return {"message": unicode(e), "ok": False}
        else:
            return {"message": version_info, "ok": True}

def get_data_source_version(self):
    if self.data_source_version_query is None:
        raise NotImplementedError
    data, error = self.run_query(self.data_source_version_query, None)
    if error is not None:
        raise Exception(error)
    try:
        version = json.loads(data)['rows'][0]['version']
    except KeyError as e:
        raise Exception(e)

    if self.data_source_version_post_process == "split by space take second":
        version = version.split(" ")[1]
    elif self.data_source_version_post_process == "split by space take last":
        version = version.split(" ")[-1]
    elif self.data_source_version_post_process == "none":
        version = version
    return version

def api_endpoint(app=None):
	BaseQueryRunner.data_source_version_query = None
	BaseQueryRunner.get_data_source_version = get_data_source_version
	PostgreSQL.data_source_version_query = "select version()"
	PostgreSQL.data_source_version_post_process = "split by space take second"
	api.add_org_resource(DataSourceVersionResource, '/api/data_sources/<data_source_id>/version')
