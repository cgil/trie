from flask import json

from trie.tests import factories
from trie.tests.base import BaseTestCase


class ProductTestCase(BaseTestCase):

    def test_get(self):
        """Test that we can get a product."""
        product = factories.ProductFactory()
        res = json.loads(self.client.get(
            '/products/{}'.format(str(product.id)),
        ).data)
        assert res['id'] == str(product.id)
