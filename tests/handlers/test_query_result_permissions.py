from redash.models import Group, db
from tests import BaseTestCase, authenticate_request

from redash_stmo.handlers.query_results.parser import extract_table_names


class TestQueryResultAPI(BaseTestCase):
    def test_query_result_query(self):
        restricted_group = self.factory.create_group(
            org=self.factory.org, type=Group.REGULAR_GROUP, name="restricted"
        )
        # Commit needed because User.group_ids is an array of IDs, not a relation
        db.session.commit()
        restricted_user = self.factory.create_user(
            group_ids=[restricted_group.id, self.factory.org.default_group.id],
            name="Restricted User",
        )
        restricted_ds = self.factory.create_data_source(
            group=restricted_group, view_only=False, type="pg"
        )
        upstream_query = self.factory.create_query(
            user=restricted_user,
            data_source=restricted_ds,
            query_text="select * from secret",
        )
        result_ds = self.factory.create_data_source(
            group=self.factory.org.default_group, view_only=False, type="results"
        )
        query = self.factory.create_query(
            user=restricted_user,
            data_source=result_ds,
            query_text="select password from query_{} limit 10".format(
                upstream_query.id
            ),
        )
        query_result = self.factory.create_query_result(
            data_source=result_ds,
            query_text=query.query_text,
            query_hash=query.query_hash,
        )
        authenticate_request(self.client, restricted_user)
        rv = self.client.get("/api/query_results/{}".format(query_result.id))
        self.assertEqual(rv.status_code, 200)

    def test_query_result_query_restrict_access(self):
        restricted_group = self.factory.create_group(
            org=self.factory.org, type=Group.REGULAR_GROUP, name="restricted"
        )
        restricted_user = self.factory.create_user(
            group_ids=[restricted_group.id, self.factory.org.default_group.id]
        )
        restricted_ds = self.factory.create_data_source(
            group=restricted_group, view_only=False, type="pg"
        )
        upstream_query = self.factory.create_query(
            user=restricted_user,
            data_source=restricted_ds,
            query_text="select * from secret",
        )
        result_ds = self.factory.create_data_source(
            group=self.factory.org.default_group, view_only=False, type="results"
        )
        query = self.factory.create_query(
            user=restricted_user,
            data_source=result_ds,
            query_text="select password from query_{}".format(upstream_query.id),
        )
        query_result = self.factory.create_query_result(
            data_source=result_ds,
            query_text=query.query_text,
            query_hash=query.query_hash,
        )
        authenticate_request(self.client, restricted_user)
        rv = self.client.get("/api/query_results/{}".format(query_result.id))
        self.assertEqual(rv.status_code, 403)

    def test_extract_table_names(self):
        query = """\
WITH standard AS (
    SELECT
        'Cold Startup from App Link' AS TestName,
        'fnprms' AS project,
        'Motorola G5' AS platform,
        NULL AS FennecValue,
        -20.0 AS Target,
        date AS TestGroupTime
    FROM cached_query_67650
    WHERE value > 0
        AND date >= datetime('now', '-56 day')
    ORDER BY TestGroupTime DESC
), fenix AS (
    SELECT
        standard.*,
        'fenix' AS BrowserTested,
        value AS CurrentValue,
        ((value - 0.511) / 0.511 * 100) AS CurrentPercent,
        (SELECT value FROM cached_query_67650 WHERE date <= datetime('now', '-7 day') ORDER BY date DESC LIMIT 1) AS LastWeekValue
    FROM cached_query_67650 AS full
        LEFT JOIN standard ON full.date = standard.TestGroupTime
    WHERE value > 0
), fennec AS (
    SELECT
        standard.*,
        'fennec' AS BrowserTested,
        standard.FennecValue AS CurrentValue,
        NULL AS CurrentPercent,
        0 AS LastWeekValue
    FROM fenix
        LEFT JOIN standard ON fenix.TestGroupTime = standard.TestGroupTime
), goal AS (
    SELECT
        standard.*,
        'target' AS BrowserTested,
        0.8 * standard.FennecValue AS CurrentValue,
        NULL AS CurrentPercent,
        0 AS LastWeekValue
    FROM fenix
        LEFT JOIN standard ON fenix.TestGroupTime = standard.TestGroupTime
),  combined AS (
    SELECT * FROM fenix
    UNION ALL
    SELECT * FROM fennec
    UNION ALL
    SELECT * FROM goal
)

SELECT
    *,
    (CurrentValue - LastWeekValue) / LastWeekValue * 100 AS OneWeekDifference
FROM combined
ORDER BY TestGroupTime DESC, BrowserTested

"""
        self.assertEqual(extract_table_names(query), ["combined"])
