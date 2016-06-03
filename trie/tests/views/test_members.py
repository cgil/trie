import copy
from decimal import Decimal

from trie.models.member import Member
from trie.tests import factories
from trie.tests.base import CRUDTestCase


class MemberTestCase(CRUDTestCase):

    def setUp(self):
        super(MemberTestCase, self).setUp()
        self.model_factory = factories.MemberFactory
        self.model = Member
        self.url_prefix = 'members'

    def test_crud(self):
        """Test members CRUD."""
        self._test_crud()

    def _test_post(self):
        """Test that we can create a new record."""
        store = factories.StoreFactory.create()
        attrs = self.model_factory.build(store=store).to_dict()
        del attrs['id']
        post_attrs = copy.deepcopy(attrs)
        post_attrs['password'] = 'fake-password'
        data = {
            'data': {
                'attributes': post_attrs,
                'type': '{}'.format(self.url_prefix),
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
        attrs = self.model_factory.build().to_dict()
        del attrs['id']
        patch_attrs = copy.deepcopy(attrs)
        del attrs['stripe_customer_id']

        data = {
            'data': {
                'attributes': patch_attrs,
                'type': '{}'.format(self.url_prefix),
                'id': str(record.id),
            }
        }
        res = self.patch(
            '/{}/{}'.format(self.url_prefix, str(record.id)),
            data=data
        )
        assert res.status_code == 200
        for k, v in attrs.iteritems():
            if k == 'price':
                assert Decimal(res.data['data']['attributes'][k]) == Decimal(v)
            else:
                assert res.data['data']['attributes'][k] == str(v)
