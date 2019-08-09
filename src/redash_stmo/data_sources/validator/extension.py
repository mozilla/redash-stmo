import subprocess

import apiclient.errors
from flask import request

from redash import models
from redash.handlers.base import BaseResource, get_object_or_404
from redash.permissions import not_view_only, has_access
from redash.utils import collect_parameters_from_request, json_loads, mustache_render

from redash_stmo.resources import add_resource


class DataSourceValidatorResource(BaseResource):

    def validate_pg(self, query_runner, query):
        p = subprocess.Popen("pgsanity", stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        stdout, _ = p.communicate(query + ";")
        return p.returncode == 0, stdout, 200

    def validate_bigquery(self, query_runner, query):
        jobs = query_runner._get_bigquery_service().jobs()
        project_id = query_runner._get_project_id()
        job_data = {
            "configuration": {
                "query": {
                    "query": query,
                },
                "dryRun": True,
            }
        }

        if query_runner.configuration.get('useStandardSql', False):
            job_data['configuration']['query']['useLegacySql'] = False

        if query_runner.configuration.get('userDefinedFunctionResourceUri'):
            resource_uris = query_runner.configuration["userDefinedFunctionResourceUri"].split(',')
            job_data["configuration"]["query"]["userDefinedFunctionResources"] = map(
                lambda resource_uri: {"resourceUri": resource_uri}, resource_uris)

        if "maximumBillingTier" in query_runner.configuration:
            job_data["configuration"]["query"]["maximumBillingTier"] = query_runner.configuration["maximumBillingTier"]

        try:
            insert_response = jobs.insert(projectId=project_id, body=job_data).execute()
        except apiclient.errors.HttpError as e:
            error = json_loads(e.content)['error']['message']
            return False, error, 200
        except Exception as e:
            return False, str(e), 500

        if 'errorResult' in insert_response['status']:
            valid = False
            response = insert_response['status']['errorResult']['error']['message']
        else:
            valid = True
            response = "This query will process %s bytes." % (insert_response['statistics']['totalBytesProcessed'],)
        return valid, response, 200

    def get_validator(self, query_runner):
        """Return the query validator for the given query runner"""
        try:
            validator = getattr(self, 'validate_%s' % query_runner.type())
            if callable(validator):
                return validator
        except AttributeError:
            pass

    def post(self, data_source_id):
        params = request.get_json(force=True)
        parameter_values = collect_parameters_from_request(request.args)
        query = mustache_render(params['query'], parameter_values)
        data_source = get_object_or_404(
            models.DataSource.get_by_id_and_org,
            data_source_id,
            self.current_org,
        )

        # get the validator method
        validator = self.get_validator(data_source.query_runner)
        if (validator is None
                or not has_access(data_source.groups, self.current_user, not_view_only)):
            return {
                'valid': False,
                'report': 'You do not have permission to run queries with this data source.'
            }, 403

        valid, report, code = validator(data_source.query_runner, query)
        return {'valid': valid, 'report': report}, code


def extension(app):
    add_resource(app, DataSourceValidatorResource, '/api/data_sources/<data_source_id>/validate')
