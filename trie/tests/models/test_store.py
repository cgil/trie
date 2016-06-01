from trie.models.store import Store
from trie.tests.base import BaseTestCase


class StoreTestCase(BaseTestCase):

    def test_store(self):
        """Test that we can initiate a store."""
        attrs = dict(
            name='name',
            tote_domain='https://www.totestore.com/name',
            domain='https://www.realstore.com/name',
            email='email@email.com',
            address_1='111 goodie st.',
            city='New York City',
            zip_code='10001',
            country='USA',
            country_code='US',
            currency='USD',
            phone='4124250015',
        )
        store = Store(**attrs)
        store.save(store)
        res = Store.get(store.id)
        for attr in attrs:
            assert getattr(res, attr) == attrs[attr]
