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

    def test_get_product_filter(self):
        """Test that we can filter returned products in a store."""
        store = self.model_factory()
        factories.ProductFactory(store=store)
        product = factories.ProductFactory(store=store)

        res = self.get(
            '/{}/{}?filter[product]={}'.format(
                self.url_prefix,
                str(store.id),
                str(product.id),
            ),
        )
        assert res.status_code == 200
        assert len(res.data['data']['attributes']['products']['data']) == 1
        assert res.data['data']['attributes']['products']['data'][0]['id'] == str(product.id)
