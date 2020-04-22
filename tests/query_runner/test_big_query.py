from redash.query_runner import query_runners
from redash_stmo.query_runner.big_query import BigQuery, parse_annotated_query
from tests import BaseTestCase


class TestBigQueryRunner(BaseTestCase):
    def test_custom_big_query_query_runner_registered(self):
        assert query_runners["bigquery"] == BigQuery

    def test_custom_big_query_query_runner_get_job_data(self, *args, **kwargs):
        query = """
            /* Task ID: 6ff0c989b3ff499193ca3fbb54225f80, Query Hash: 56888d88acb5475b95484eeb005f8e5f, Query ID: 12345, Queue: default, Username: jezdez */

            SELECT * FROM users;
        """
        with self.app.test_request_context("/"):
            self.app.preprocess_request()
            query_runner = BigQuery({})
            job_data = query_runner._get_job_data(query)
            assert job_data["labels"] == {
                "App": "redash",
                "Name": "localhost:5000/queries/12345",
                "Query Hash": "56888d88acb5475b95484eeb005f8e5f",
                "Query ID": "12345",
                "Queue": "default",
                "Task ID": "6ff0c989b3ff499193ca3fbb54225f80",
                "Username": "jezdez",
            }

    def test_parse_annotated_query_success(self):
        query = """
            /* Task ID: 5b7efa616d474a54874d337cc27f1953, Query Hash: 93ff42fc6ac443bfba222553890b4124, Query ID: 12345, Queue: default, Username: jezdez */

            SELECT * FROM users;
        """
        result = {
            "Query Hash": "93ff42fc6ac443bfba222553890b4124",
            "Query ID": "12345",
            "Queue": "default",
            "Task ID": "5b7efa616d474a54874d337cc27f1953",
            "Username": "jezdez",
        }
        assert parse_annotated_query(query) == result

    def test_parse_annotated_query_no_annotation(self):
        assert parse_annotated_query("") == {}
        assert parse_annotated_query("SELECT * FROM users;") == {}

    def test_parse_annotated_query_wrong_annotation(self):
        query = """
            /* Task ID: 8ccd40c878f59fa69ccf31a72140b208, Query Hash: f6bf37efedbc0a2dfffc1caf5088d86e, Query ID: 12345, Queue: default, Username: jezdez

            SELECT * FROM users;
        """
        result = {}
        assert parse_annotated_query(query) == result
