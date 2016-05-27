import uuid

from trie.models.product import Product
from trie.schemas.products_schema import ProductsSchema
from trie.tests import factories
from trie.tests.base import ViewTestCase


class ProductTestCase(ViewTestCase):

    def test_get(self):
        """Test that we can get a product."""
        product = factories.ProductFactory()
        res = self.get(
            '/products/{}'.format(str(product.id)),
        )
        assert res.data['data']['id'] == str(product.id)
        assert res.status_code == 200

    def test_get_404(self):
        """Test that we can get a product 404's."""
        res = self.get(
            '/products/{}'.format(str(uuid.uuid4())),
        )
        assert res.status_code == 404

    def test_get_list(self):
        """Test that we can get a product."""
        products = factories.ProductFactory.create_batch(size=3)
        res = self.get(
            '/products/',
        )
        assert res.status_code == 200
        found = Product.query.all()
        found = sorted(found, key=lambda p: p.id)
        products = sorted(products, key=lambda p: p.id)
        for i, f in enumerate(found):
            assert found[i].id == products[i].id

    def test_post(self):
        """Test that we can create a new product."""
        data = {
            'data': {
                'attributes': {
                    'title': 'title_test',
                    'description': 'description_test',
                    'price': 123.45,
                    'image': 'https://www.image.com/test',
                },
                'type': 'products',
            }
        }
        res = self.post(
            '/products/',
            data=data,
        )
        schema = ProductsSchema()
        schema.validate(res.data)
        for k, v in data['data']['attributes'].iteritems():
            assert str(res.data['data']['attributes'][k]) == str(v)
        assert res.status_code == 201

    def test_delete(self):
        """Test that we can delete a product."""
        product = factories.ProductFactory()
        assert len(Product.query.all()) == 1
        res = self.delete(
            '/products/{}'.format(str(product.id))
        )
        found = Product.query.all()
        assert len(found) == 1
        assert found[0].deleted_at is not None
        assert res.status_code == 204
        assert not res.data

    def test_patch(self):
        """Test that we can patch a product."""
        product = factories.ProductFactory()
        data = {
            'data': {
                'attributes': {
                    'title': 'title_patch_test',
                },
                'type': 'products',
                'id': str(product.id),
            }
        }
        res = self.patch(
            '/products/{}'.format(str(product.id)),
            data=data
        )
        assert res.status_code == 200
        assert (
            res.data['data']['attributes']['title'] ==
            data['data']['attributes']['title']
        )
