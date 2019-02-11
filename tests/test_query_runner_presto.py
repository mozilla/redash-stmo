from pyhive import presto
from redash.query_runner import query_runners

from redash_stmo.query_runner.presto import STMOPresto, stmo_connect


def test_custom_presto_query_runner():
    assert query_runners['presto'] == STMOPresto


def test_custom_presto_connect():
    assert presto.connect == stmo_connect
