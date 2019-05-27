from redash.query_runner import query_runners

from redash_stmo.query_runner.big_query import STMOBigQuery, parse_annotated_query

annotated_query = """
    /* Task ID: 8ccd40c878f59fa69ccf31a72140b208, Query Hash: f6bf37efedbc0a2dfffc1caf5088d86e, Query ID: 12345, Queue: celery, Username: jezdez */

    SELECT * FROM users;
"""


def test_custom_big_query_query_runner_registered():
    assert query_runners['bigquery'] == STMOBigQuery


def test_custom_big_query_query_runner_get_job_data():
    query_runner = STMOBigQuery({})
    job_data = query_runner._get_job_data(annotated_query)
    assert job_data == {}


def test_parse_annotated_query_success():
    assert parse_annotated_query(annotated_query) == {
        'Query Hash': 'f6bf37efedbc0a2dfffc1caf5088d86e',
        'Query ID': '12345',
        'Queue': 'celery',
        'Task ID': '8ccd40c878f59fa69ccf31a72140b208',
        'Username': 'jezdez',
    }


def test_parse_annotated_query_no_annotation():
    assert parse_annotated_query("") == {}
    assert parse_annotated_query("SELECT * FROM users;") == {}


def test_parse_annotated_query_wrong_annotation():
    query = """
        /* Task ID: 8ccd40c878f59fa69ccf31a72140b208, Query Hash: f6bf37efedbc0a2dfffc1caf5088d86e, Query ID: 12345, Queue: celery, Username: jezdez

        SELECT * FROM users;
    """
    assert parse_annotated_query(query) == {}
