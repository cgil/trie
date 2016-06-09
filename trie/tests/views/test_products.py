from decimal import Decimal

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

    def _test_post(self):
        """Test that we can create a new record."""
        store = factories.StoreFactory.create()
        attrs = self.model_factory.build(store=store)
        del attrs['id']
        data = {
            'data': {
                'attributes': attrs,
                'type': '{}'.format(self.url_prefix),
                'relationships': {
                    'store': {
                        'data': {'type': 'stores', 'id': str(store.id)}
                    }
                },
            }
        }
        res = self.post(
            '/{}/'.format(self.url_prefix),
            data=data,
        )
        for k, v in attrs.iteritems():
            if k == 'price':
                assert Decimal(res.data['data']['attributes'][k]) == Decimal(v)
            elif not k.endswith('id'):
                assert res.data['data']['attributes'][k] == str(v)
        assert res.status_code == 201

    def _test_patch(self):
        """Test that we can patch a record."""
        record = self.model_factory()
        attrs = self.model_factory.build()
        del attrs['id']
        del attrs['store_id']

        data = {
            'data': {
                'attributes': attrs,
                'type': '{}'.format(self.url_prefix),
                'id': str(record.id),
            }
        }
        res = self.patch(
            '/{}/{}'.format(self.url_prefix, str(record.id)),
            data=data,
        )
        assert res.status_code == 200
        for k, v in attrs.iteritems():
            if k == 'price':
                assert Decimal(res.data['data']['attributes'][k]) == Decimal(v)
            else:
                assert res.data['data']['attributes'][k] == str(v)
