from trie.models.store import Store
from trie.tests import factories
from trie.tests.base import CRUDTestCase


class StoreTestCase(CRUDTestCase):

    def setUp(self):
        super(StoreTestCase, self).setUp()
        self.model_factory = factories.StoreFactory
        self.model = Store
        self.url_prefix = 'stores'

    def test_crud(self):
        """Test stores CRUD."""
        self._test_crud()
