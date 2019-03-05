import subprocess
import tempfile

from flask import make_response, request

from redash import models
from redash.handlers.base import BaseResource, get_object_or_404
from redash.utils import collect_parameters_from_request, json_loads, mustache_render
from redash.permissions import not_view_only, has_access
from redash.query_runner import BaseSQLQueryRunner, pg, big_query
from redash_stmo.resources import add_resource

import apiclient.errors

class QueryValidatorResource(BaseResource):
    def post(self):
        params = request.get_json(force=True)
        parameter_values = collect_parameters_from_request(request.args)
        query = mustache_render(params['query'], parameter_values)
        data_source = get_object_or_404(models.DataSource.get_by_id_and_org, params.get('data_source_id'), self.current_org)

        if not has_access(data_source.groups, self.current_user, not_view_only):
            return {'valid': False, 'report': 'You do not have permission to run queries with this data source.'}, 403

        try:
            valid, report = data_source.query_runner.validate(query)
            return {'valid': valid, 'report': report}, 200
        except apiclient.errors.HttpError as e:
            if e.resp.status == 400:
                error = json_loads(e.content)['error']['message']
            else:
                error = e.content
            return {'valid': False, 'report': error }, 200
        except Exception as e:
            return {'valid': False, 'report': str(e)}, 500


def validate_pg(self, query):
    p = subprocess.Popen("pgsanity", stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    stdout, _ = p.communicate(query + ";")
    return p.returncode == 0, stdout


def validate_bigquery(self, query):
        jobs = self._get_bigquery_service().jobs()
        project_id = self._get_project_id()
        job_data = {
            "configuration": {
                "query": {
                    "query": query,
                },
                "dryRun": True,
            }
        }

        if self.configuration.get('useStandardSql', False):
            job_data['configuration']['query']['useLegacySql'] = False

        if self.configuration.get('userDefinedFunctionResourceUri'):
            resource_uris = self.configuration["userDefinedFunctionResourceUri"].split(',')
            job_data["configuration"]["query"]["userDefinedFunctionResources"] = map(
                lambda resource_uri: {"resourceUri": resource_uri}, resource_uris)

        if "maximumBillingTier" in self.configuration:
            job_data["configuration"]["query"]["maximumBillingTier"] = self.configuration["maximumBillingTier"]

        insert_response = jobs.insert(projectId=project_id, body=job_data).execute()
        if 'errorResult' in insert_response['status']:
            return False, insert_response['status']['errorResult']
        return True, "This query will process %s bytes." % (insert_response['statistics']['totalBytesProcessed'],)


def extension(app=None):
    add_resource(app, QueryValidatorResource, '/api/query_check')
    pg.PostgreSQL.validate = validate_pg
    big_query.BigQuery.validate = validate_bigquery
