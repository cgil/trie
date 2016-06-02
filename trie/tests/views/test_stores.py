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

    def test_misc_get(self):
        """Test getting a store."""
        store = self.model_factory()
        factories.ProductFactory.create_batch(size=3, store=store)
        res = self.get(
            '/{}'.format(
                str(store.id),
            ),
        )
        assert res.data['data']['id'] == str(store.id)
        assert res.status_code == 200
