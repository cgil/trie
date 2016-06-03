from decimal import Decimal

from trie.models.product import Product
from trie.tests import factories
from trie.tests.base import BaseTestCase


class ProductTestCase(BaseTestCase):

    def test_product(self):
        """Test that we can initiate a product."""
        store = factories.StoreFactory()
        attrs = dict(
            title='title',
            description='description',
            image='https://www.image.com/123',
            price=Decimal(123.45),
            store_id=store.id,
        )
        product = Product(**attrs)

        product = Product(**attrs)
        product.save(product)
        res = Product.get(product.id)
        for attr in attrs:
            assert getattr(res, attr) == attrs[attr]
