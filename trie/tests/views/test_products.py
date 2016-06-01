from trie.models.product import Product
from trie.tests import factories
from trie.tests.base import CRUDTestCase


class ProductTestCase(CRUDTestCase):

    def setUp(self):
        super(ProductTestCase, self).setUp()
        self.model_factory = factories.ProductFactory
        self.model = Product
        self.url_prefix = 'products'

    def test_crud(self):
        """Test products CRUD."""
        self._test_crud()
