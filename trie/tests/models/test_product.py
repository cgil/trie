from trie.models.product import Product
from trie.tests.base import BaseTestCase


class ProductTestCase(BaseTestCase):

    def test_product(self):
        """Test that we can initiate a product."""
        attrs = dict(
            title='title',
            description='description',
            image='https://www.image.com/123',
            price=12345,
        )
        product = Product(**attrs)

        product = Product(**attrs)
        product.save(product)
        res = Product.get(product.id)
        for attr in attrs:
            assert getattr(res, attr) == attrs[attr]
