from redash.query_runner import query_runners

from redash_stmo.query_runner.big_query import BigQuery, parse_annotated_query

from tests import BaseTestCase


class TestBigQueryRunner(BaseTestCase):
    annotated_query = """
        /* Task ID: 8ccd40c878f59fa69ccf31a72140b208, Query Hash: f6bf37efedbc0a2dfffc1caf5088d86e, Query ID: 12345, Queue: celery, Username: jezdez */

        SELECT * FROM users;
    """

    def test_custom_big_query_query_runner_registered(self):
        assert query_runners["bigquery"] == BigQuery

    def test_custom_big_query_query_runner_get_job_data(self, *args, **kwargs):
        with self.app.test_request_context("/"):
            self.app.preprocess_request()
            query_runner = BigQuery({})
            job_data = query_runner._get_job_data(self.annotated_query)
            assert job_data["labels"] == {
                "App": "redash",
                "Name": "https://localhost:5000/default/queries/12345",
                "Query Hash": "f6bf37efedbc0a2dfffc1caf5088d86e",
                "Query ID": "12345",
                "Queue": "celery",
                "Task ID": "8ccd40c878f59fa69ccf31a72140b208",
                "Username": "jezdez",
            }

    def test_parse_annotated_query_success(self):
        assert parse_annotated_query(self.annotated_query) == {
            "Query Hash": "f6bf37efedbc0a2dfffc1caf5088d86e",
            "Query ID": "12345",
            "Queue": "celery",
            "Task ID": "8ccd40c878f59fa69ccf31a72140b208",
            "Username": "jezdez",
        }

    def test_parse_annotated_query_no_annotation(self):
        assert parse_annotated_query("") == {}
        assert parse_annotated_query("SELECT * FROM users;") == {}

    def test_parse_annotated_query_wrong_annotation(self):
        query = """
            /* Task ID: 8ccd40c878f59fa69ccf31a72140b208, Query Hash: f6bf37efedbc0a2dfffc1caf5088d86e, Query ID: 12345, Queue: celery, Username: jezdez

            SELECT * FROM users;
        """
        assert parse_annotated_query(query) == {}
