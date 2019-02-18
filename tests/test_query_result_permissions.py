from tests import BaseTestCase

from redash.models import db, Group


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
        rv = self.make_request(
            "get", "/api/query_results/{}".format(query_result.id), user=restricted_user
        )
        self.assertEquals(rv.status_code, 200)

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
        rv = self.make_request("get", "/api/query_results/{}".format(query_result.id))
        self.assertEquals(rv.status_code, 403)
