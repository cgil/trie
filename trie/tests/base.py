import json
import unittest


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
