import logging
import re

from redash.utils import base_url
from redash.authentication.org_resolving import current_org
from redash.query_runner import register
from redash.query_runner.big_query import BigQuery as RedashBigQuery

logger = logging.getLogger(__name__)


ANNOTATION_RE = re.compile(r"^\/\*\s(.*)\s\*\/$", re.U | re.M)


def parse_annotated_query(query):
    """
    Parses the given query for the annotation that Redash left
    there when before running the job.

    E.g. a query that has the annotation on top::

        /* Task ID: 8ccd40c878f59fa69ccf31a72140b208, Query Hash: f6bf37efedbc0a2dfffc1caf5088d86e, Query ID: 12345, Queue: celery, Username: jezdez */

        SELECT * FROM users;

    will lead to returning::

        {
            'Query Hash': 'f6bf37efedbc0a2dfffc1caf5088d86e',
            'Query ID': '12345',
            'Queue': 'celery',
            'Task ID': '8ccd40c878f59fa69ccf31a72140b208',
            'Username': 'jezdez',
        }

    which we can use as labels when submitting the BigQuery job.
    """
    if not query or "/*" not in query:
        return {}
    match = ANNOTATION_RE.match(query.strip())
    if not match:
        return {}
    # Split by comma and colons to create a key/value dict of query annotations
    return dict(map(lambda s: map(str.strip, s.split(":")), match.group(1).split(",")))


class BigQuery(RedashBigQuery):

    @classmethod
    def type(cls):
        """Overrides the name to match the name of the parent query runner"""
        return 'bigquery'

    @classmethod
    def annotate_query(cls):
        """Needed so we can extract annotations from query for job labels"""
        return True

    def __init__(self, *args, **kwargs):
        super(BigQuery, self).__init__(*args, **kwargs)
        self._query_user = None

    def _get_job_data(self, query):
        job_data = super(BigQuery, self)._get_job_data(query)
        labels = {"App": "redash"}

        # Add the Owner label with the current user's email address
        if self._query_user is not None:
            labels["Owner"] = self._query_user.email

        # Add all the parsed query metadata as labels to the job
        parsed_annotation = parse_annotated_query(query)
        labels.update(parsed_annotation)

        # Add a full URL to the query for the "Name" label
        if "Query ID" in parsed_annotation:
            host = base_url(current_org)
            labels["Name"] = "{host}/queries/{query_id}".format(
                host=host, query_id=parsed_annotation["Query ID"]
            )

        if labels:
            job_data["labels"] = labels

        return job_data

    def run_query(self, query, user):
        # Storing the query's user in an instance variable for use
        # in the custom job label.
        self._query_user = user
        return super(BigQuery, self).run_query(query, user)


def extension(app):
    logger.info("Loading Redash Extension for the custom BigQuery query runner")
    # Register our own BigQuery query runner class
    # which automatically overwrites the default presto query runner
    register(BigQuery)
    logger.info("Loaded Redash Extension for the custom BigQuery query runner")
    return
