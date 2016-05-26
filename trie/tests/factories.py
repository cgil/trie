import logging
from trie import db

import factory

from trie.models.product import Product

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
