from redash.handlers.query_results import QueryResultResource
from redash.permissions import require_access, require_permission, view_only
from redash.handlers.base import get_object_or_404
from redash import models

from ...resources import add_resource
from .parser import extract_table_names


class StmoQueryResultResource(QueryResultResource):
    @require_permission('view_query')
    def get(self, query_id=None, query_result_id=None, filetype='json'):
        if query_result_id:
            query_result = get_object_or_404(
                models.QueryResult.get_by_id_and_org,
                query_result_id,
                self.current_org,
            )
            # Look for queries matching this result whose data source is 'Query Results'.
            if models.Query.query.join(
                models.DataSource,
            ).filter(
                models.Query.query_hash == query_result.query_hash,
                models.DataSource.type == 'results',
            ).first():
                table_names = extract_table_names(query_result.query_text)
                for table_name in table_names:
                    # Look for query IDs being accessed.
                    if table_name.startswith("query_"):
                        try:
                            qid = int(table_name.split('_', 1)[1])
                        except ValueError:
                            # If it's not "query_NNN" it can't affect our permissions check here.
                            continue
                        upstream_q = models.Query.query.filter(
                            models.Query.id == qid
                        ).first()
                        if upstream_q is None:
                            continue
                        # If the user making this request doesn't have permission to
                        # view the query results being accessed in this query, deny
                        # access.
                        require_access(upstream_q.data_source.groups, self.current_user, view_only)

            require_access(query_result.data_source.groups, self.current_user, view_only)

        return super(StmoQueryResultResource, self).get(query_id, query_result_id, filetype)


def extension(app):
    # remove the original resource
    del app.view_functions['query_result']
    add_resource(
        app,
        StmoQueryResultResource,
        '/api/query_results/<query_result_id>.<filetype>',
        '/api/query_results/<query_result_id>',
        '/api/queries/<query_id>/results.<filetype>',
        '/api/queries/<query_id>/results/<query_result_id>.<filetype>',
        endpoint='query_result',
    )
