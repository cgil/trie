from trie import db
from trie.models.product import Product
from trie.tests.base import BaseTestCase


class ProductTestCase(BaseTestCase):

    def test_product(self):
        """Test that we can initiate a product."""
        product = Product(
            title='title',
            description='description',
            image='https://www.image.com/123',
            price=12345,
        )

        db.session.add(product)
        db.session.commit()
        res = Product.get(product.id).one()
        assert res.title == 'title'
        assert res.description == 'description'
        assert res.image == 'https://www.image.com/123'
        assert res.price == 12345
