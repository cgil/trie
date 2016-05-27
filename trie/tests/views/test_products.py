from trie.tests import factories
from trie.tests.base import ViewTestCase
from trie.schemas.products_schema import ProductsSchema


class ProductTestCase(ViewTestCase):

    def test_get(self):
        """Test that we can get a product."""
        product = factories.ProductFactory()
        res = self.get(
            '/products/{}'.format(str(product.id)),
        )
        assert res.data['id'] == str(product.id)
        assert res.status_code == 200

    def test_post(self):
        """Test that we can create a new product."""
        attributes = {
            'title': 'title',
            'description': 'description',
            'price': 12345,
            'image': 'https://www.image.com/test',
        }
        res = self.post(
            '/products/',
            data={
                'data': {
                    'attributes': attributes
                }
            }
        )
        schema = ProductsSchema()
        schema.validate(res.data)
        attrs = schema.dump(attributes).data
        for k, v in attrs.iteritems():
            assert res.data[k] == v
        assert res.status_code == 201
