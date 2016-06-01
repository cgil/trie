import logging

import factory

from trie import db
from trie.models.product import Product
from trie.models.store import Store

logging.getLogger('factory').setLevel(logging.ERROR)


class BaseFactory(factory.alchemy.SQLAlchemyModelFactory):

    """Base Factory."""

    class Meta:
        abstract = True
        sqlalchemy_session = db.session

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Overrides create strategy, commits on create"""
        obj = model_class(*args, **kwargs)
        obj.save(obj)
        return obj


class ProductFactory(BaseFactory):

    class Meta:
        model = Product

    description = factory.Sequence(lambda n: 'descripton_{0}'.format(n))
    image = factory.Sequence(lambda n: 'https://www.image.com/test_{0}.png'.format(n))
    price = factory.Sequence(lambda n: 2000 + n)
    title = factory.Sequence(lambda n: 'title_{0}'.format(n))


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
