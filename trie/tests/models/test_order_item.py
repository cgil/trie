from trie.models.order_item import OrderItem
from trie.tests import factories
from trie.tests.base import BaseTestCase


class OrderItemTestCase(BaseTestCase):

    def test_order_item(self):
        """Test that we can initiate a order_item."""
        store = factories.StoreFactory()
        member = factories.MemberFactory()
        order = factories.OrderFactory(member=member, store=store)
        product = factories.ProductFactory(store=store)
        attrs = dict(
            quantity=3,
            order_id=order.id,
            product_id=product.id,
            member_id=member.id,
            store_id=store.id,
        )
        order_item = OrderItem(**attrs)
        order_item.save(order_item)
        res = OrderItem.get(order_item.id)
        for attr in attrs:
            assert getattr(res, attr) == attrs[attr]
