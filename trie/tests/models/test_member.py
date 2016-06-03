from trie.models.member import Member
from trie.tests.base import BaseTestCase


class MemberTestCase(BaseTestCase):

    def test_member(self):
        """Test that we can initiate a member."""
        attrs = dict(
            email='name@awesome.com',
            password='supercoolpassword',
            stripe_customer_id='secret-stripe-customer-id',
        )
        member = Member(**attrs)
        member.save(member)
        res = Member.get(member.id)
        for attr in attrs:
            assert getattr(res, attr) == attrs[attr]
