from decimal import Decimal
import datetime
import json
import unittest
import uuid


from trie import create_app
from trie import db


class ViewTestCaseResponse(object):
    """Wraps a response object to easily extract and manipulate fields."""

    def __init__(self, response):
        self.data = json.loads(response.get_data() or '{}')
        self.status_code = response.status_code


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['DEBUG'] = True
        self.app.config['TESTING'] = True
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()


class ViewTestCase(BaseTestCase):

    def setUp(self):
        super(ViewTestCase, self).setUp()
        self.client = self.app.test_client()

    def post(self, url, data=None):
        """Perform a post request."""
        res = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        return ViewTestCaseResponse(res)

    def get(self, url):
        """Perform a get request."""
        res = self.client.get(url)
        return ViewTestCaseResponse(res)

    def delete(self, url):
        """Perform a delete request."""
        res = self.client.delete(url)
        return ViewTestCaseResponse(res)

    def patch(self, url, data=None):
        """Perform a patch request."""
        res = self.client.patch(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        return ViewTestCaseResponse(res)


class CRUDTestCase(ViewTestCase):

    def setUp(self):
        super(CRUDTestCase, self).setUp()

    def _test_crud(self):
        """Run all the CRUD tests."""
        for test in [
            self._test_get,
            self._test_get_404,
            self._test_get_soft_deleted,
            self._test_get_list,
            self._test_get_list_soft_deleted,
            self._test_post,
            self._test_delete,
            self._test_patch,
        ]:
            self.tearDown()
            self.setUp()
            test()

    def _test_get(self):
        """Test that we can get a record."""
        record = self.model_factory()
        res = self.get(
            '/{}/{}'.format(
                self.url_prefix,
                str(record.id),
            ),
        )
        assert res.data['data']['id'] == str(record.id)
        assert res.status_code == 200

    def _test_get_404(self):
        """Test that we can get a record 404's."""
        res = self.get(
            '/{}/{}'.format(
                self.url_prefix,
                str(uuid.uuid4()),
            ),
        )
        assert res.status_code == 404

    def _test_get_soft_deleted(self):
        """Test that we can get a record."""
        record = self.model_factory()
        record.deleted_at = datetime.datetime.utcnow()
        res = self.get(
            '/{}/{}'.format(
                self.url_prefix,
                str(record.id)
            ),
        )
        assert res.status_code == 404

    def _test_get_list(self):
        """Test that we can get a record."""
        records = self.model_factory.create_batch(size=3)
        res = self.get(
            '/{}/'.format(self.url_prefix),
        )
        assert res.status_code == 200
        found = self.model.query.all()
        assert len(found) == 3
        found = sorted(found, key=lambda p: p.id)
        records = sorted(records, key=lambda p: p.id)
        for i, f in enumerate(found):
            assert found[i].id == records[i].id

    def _test_get_list_soft_deleted(self):
        """Test that we can get a record."""
        records = self.model_factory.create_batch(size=3)
        for record in records:
            record.deleted_at = datetime.datetime.utcnow()
        res = self.get(
            '/{}/'.format(self.url_prefix),
        )
        assert res.status_code == 200
        assert not res.data['data']

    def _test_post(self):
        """Test that we can create a new record."""
        stub = self.model_factory.stub()
        data = {
            'data': {
                'attributes': stub.__dict__,
                'type': '{}'.format(self.url_prefix),
            }
        }
        res = self.post(
            '/{}/'.format(self.url_prefix),
            data=data,
        )
        for k, v in stub.__dict__.iteritems():
            if k == 'price':
                assert Decimal(res.data['data']['attributes'][k]) == Decimal(v)
            else:
                assert res.data['data']['attributes'][k] == str(v)
        assert res.status_code == 201

    def _test_delete(self):
        """Test that we can delete a record."""
        record = self.model_factory()
        assert len(self.model.query.all()) == 1
        res = self.delete(
            '/{}/{}'.format(self.url_prefix, str(record.id))
        )
        found = self.model.query.all()
        assert len(found) == 1
        assert found[0].deleted_at is not None
        assert res.status_code == 204
        assert not res.data

    def _test_patch(self):
        """Test that we can patch a record."""
        record = self.model_factory()
        stub = self.model_factory.stub()
        data = {
            'data': {
                'attributes': stub.__dict__,
                'type': '{}'.format(self.url_prefix),
                'id': str(record.id),
            }
        }
        res = self.patch(
            '/{}/{}'.format(self.url_prefix, str(record.id)),
            data=data
        )
        assert res.status_code == 200
        for k, v in stub.__dict__.iteritems():
            if k == 'price':
                assert Decimal(res.data['data']['attributes'][k]) == Decimal(v)
            else:
                assert res.data['data']['attributes'][k] == str(v)
