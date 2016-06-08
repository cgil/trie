import datetime
import logging

import factory

from trie import db
from trie.models.member import Member
from trie.models.order import Order
from trie.models.order_item import OrderItem
from trie.models.product import Product
from trie.models.role import Role
from trie.models.store import Store

logging.getLogger('factory').setLevel(logging.ERROR)


class BaseFactory(factory.alchemy.SQLAlchemyModelFactory):

    """Base Factory."""

    class Meta:
        abstract = True
        sqlalchemy_session = db.session

    @classmethod
    def _build(cls, model_class, *args, **kwargs):
        for k in kwargs.keys():
            if k in model_class.relationships():
                rel_key = '{}_id'.format(k)
                kwargs[rel_key] = str(kwargs[k].id)
        return super(BaseFactory, cls)._build(model_class, *args, **kwargs)

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Overrides create strategy, commits on create"""
        for k in kwargs.keys():
            if k in model_class.relationships():
                rel_key = '{}_id'.format(k)
                kwargs[rel_key] = str(kwargs[k].id)
        obj = super(BaseFactory, cls)._create(model_class, *args, **kwargs)
        obj.save(obj)
        return obj


class StoreFactory(BaseFactory):

    class Meta:
        model = Store

    name = factory.Sequence(lambda n: 'name_{0}'.format(n))
    tote_domain = factory.Sequence(lambda n: 'https://www.totestore.com/name_{0}'.format(n))
    domain = factory.Sequence(lambda n: 'https://www.external-domain-{0}.com/'.format(n))
    email = factory.Sequence(lambda n: 'name_{0}@domain.com'.format(n))
    address_1 = factory.Faker('street_address')
    city = factory.Faker('city')
    zip_code = factory.Faker('zipcode')
    country = factory.Faker('country')
    country_code = factory.Faker('country_code')
    currency = factory.Faker('currency_code')
    phone = factory.Sequence(lambda n: '412400110{0}'.format(n))


class ProductFactory(BaseFactory):

    class Meta:
        model = Product

    description = factory.Sequence(lambda n: 'descripton_{0}'.format(n))
    image = factory.Sequence(lambda n: 'https://www.image.com/test_{0}.png'.format(n))
    price = factory.Sequence(lambda n: 2000 + n)
    title = factory.Sequence(lambda n: 'title_{0}'.format(n))

    store = factory.SubFactory(StoreFactory)


class MemberFactory(BaseFactory):

    class Meta:
        model = Member

    email = factory.Sequence(lambda n: 'name_{0}@domain.com'.format(n))
    password = factory.Faker('password')
    stripe_customer_id = factory.Faker('sha1')

    active = True
    confirmed_at = factory.LazyFunction(datetime.datetime.now)
    current_login_at = factory.LazyFunction(datetime.datetime.now)
    current_login_ip = factory.Faker('ipv4')
    last_login_at = factory.LazyFunction(datetime.datetime.now)
    last_login_ip = factory.Faker('ipv4')
    login_count = factory.Sequence(lambda n: n)


class OrderFactory(BaseFactory):

    class Meta:
        model = Order

    financial_status = factory.Iterator(['paid', 'voided', 'refunded'])
    fulfillment_status = factory.Iterator(['fulfilled', 'partial'])
    total_price = factory.Sequence(lambda n: 2000 + n)
    shipping_address_city = factory.Faker('city')
    shipping_address_country = factory.Faker('country')
    shipping_address_country_code = factory.Faker('country_code')
    shipping_address_1 = factory.Faker('street_address')
    shipping_address_zip = factory.Faker('zipcode')
    shipping_name = factory.Faker('name')

    store = factory.SubFactory(StoreFactory)
    member = factory.SubFactory(MemberFactory)


class OrderItemFactory(BaseFactory):

    class Meta:
        model = OrderItem

    quantity = factory.Sequence(lambda n: n)
    store = factory.SubFactory(StoreFactory)
    member = factory.SubFactory(MemberFactory)
    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory(ProductFactory)


class RoleFactory(BaseFactory):

    class Meta:
        model = Role

    name = factory.Sequence(lambda n: 'name_{0}'.format(n))
    description = factory.Sequence(lambda n: 'descripton_{0}'.format(n))
