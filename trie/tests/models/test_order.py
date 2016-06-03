from decimal import Decimal

from trie.tests import factories
from trie.models.order import Order
from trie.tests.base import BaseTestCase


class OrderTestCase(BaseTestCase):

    def test_order(self):
        """Test that we can initiate a order."""

        member = factories.MemberFactory()
        store = factories.StoreFactory()
        attrs = dict(
            financial_status='paid',
            fulfillment_status='fulfilled',
            total_price=Decimal(123.55),
            member_id=member.id,
            store_id=store.id,
        )
        order = Order(**attrs)
        order.save(order)
        res = Order.get(order.id)
        for attr in attrs:
            assert getattr(res, attr) == attrs[attr]
