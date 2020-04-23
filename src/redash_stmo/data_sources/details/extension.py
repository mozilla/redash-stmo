import json
import logging
from redash.handlers.base import BaseResource, get_object_or_404
from redash.models import DataSource
from redash.permissions import require_access, view_only
from redash_stmo.resources import add_resource


DATASOURCE_URLS = {
    "bigquery": "https://cloud.google.com/bigquery/docs/reference/standard-sql/functions-and-operators",
    "Cassandra": "http://cassandra.apache.org/doc/latest/cql/index.html",
    "dynamodb_sql": "https://dql.readthedocs.io/en/latest/",
    "baseelasticsearch": "https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html",
    "google_spreadsheets": "http://redash.readthedocs.io/en/latest/datasources.html#google-spreadsheets",
    "hive": "https://cwiki.apache.org/confluence/display/Hive/LanguageManual",
    "impala": "http://www.cloudera.com/documentation/enterprise/latest/topics/impala_langref.html",
    "influxdb": "https://docs.influxdata.com/influxdb/v1.0/query_language/spec/",
    "jirajql": "https://confluence.atlassian.com/jirasoftwarecloud/advanced-searching-764478330.html",
    "mongodb": "https://docs.mongodb.com/manual/reference/operator/query/",
    "mssql": "https://msdn.microsoft.com/en-us/library/bb510741.aspx",
    "mysql": "https://dev.mysql.com/doc/refman/5.7/en/",
    "oracle": "http://docs.oracle.com/database/121/SQLRF/toc.htm",
    "pg": "https://www.postgresql.org/docs/current/",
    "redshift": "http://docs.aws.amazon.com/redshift/latest/dg/cm_chap_SQLCommandRef.html",
    "presto": "https://prestodb.io/docs/current/",
    "python": "http://redash.readthedocs.io/en/latest/datasources.html#python",
    "insecure_script": "http://redash.readthedocs.io/en/latest/datasources.html#python",
    "sqlite": "http://sqlite.org/lang.html",
    "treasuredata": "https://docs.treasuredata.com/categories/hive",
    "url": "http://redash.readthedocs.io/en/latest/datasources.html#url",
    "vertica": (
        "https://my.vertica.com/docs/8.0.x/HTML/index.htm#Authoring/"
        "ConceptsGuide/Other/SQLOverview.htm%3FTocPath%3DSQL"
        "%2520Reference%2520Manual%7C_____1"
    ),
}


DATASOURCE_VERSION_PARSE_INFO = {
    "pg": {"version_query": "SELECT version();", "delimiter": " ", "index": 1},
    "redshift": {"version_query": "SELECT version();", "delimiter": " ", "index": -1},
    "mysql": {
        "version_query": "SELECT VERSION() AS version;",
        "delimiter": "-",
        "index": 0,
    },
}

logger = logging.getLogger(__name__)


def get_data_source_version(query_runner):
    parse_info = DATASOURCE_VERSION_PARSE_INFO.get(query_runner.type())
    if parse_info is None:
        return None

    data, error = query_runner.run_query(parse_info["version_query"], None)
    if error is not None:
        logger.error(
            "Unable to run version query for %s: %s", query_runner.type(), error
        )
        return None
    try:
        version = json.loads(data)["rows"][0]["version"]
    except (KeyError, IndexError) as err:
        logger.exception(
            "Unable to parse data source version for %s: %s", query_runner.type(), err
        )
        return None

    version = version.split(parse_info["delimiter"])[parse_info["index"]]
    return version


class DataSourceDetailsResource(BaseResource):
    def get(self, data_source_id):
        data_source = get_object_or_404(
            DataSource.get_by_id_and_org, data_source_id, self.current_org
        )
        require_access(data_source.groups, self.current_user, view_only)
        try:
            result = {
                "type_name": data_source.query_runner.name(),
                "doc_url": DATASOURCE_URLS.get(data_source.query_runner.type(), None),
                "version": get_data_source_version(data_source.query_runner),
            }
        except Exception as e:
            return {"message": str(e), "ok": False}
        else:
            return {"message": result, "ok": True}


def extension(app=None):
    add_resource(
        app, DataSourceDetailsResource, "/api/data_sources/<data_source_id>/details"
    )
