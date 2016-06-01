from flask import Blueprint
from flask import make_response
from flask import request
from flask_restful import Api
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from trie import db
from trie.models.product import Product
from trie.schemas.products_schema import ProductsSchema


products_schema = ProductsSchema()
products_blueprint = Blueprint('products', __name__, url_prefix='/products')
api = Api(products_blueprint)


class ProductsListAPI(Resource):

    def get(self):
        products = Product.query.filter(Product.deleted_at.is_(None)).all()
        results = products_schema.dump(products, many=True).data
        return results

    def post(self):
        raw_dict = request.get_json(force=True)
        try:
            products_schema.validate(raw_dict)
            product_dict = raw_dict['data']['attributes']
            product = Product(
                title=product_dict['title'],
                description=product_dict['description'],
                image=product_dict['image'],
                price=product_dict['price'],
            )
            product.save(product)
            query = Product.query.get(product.id)
            result = products_schema.dump(query).data
            return result, 201

        except ValidationError as err:
                return {'error': err.messages}, 403

        except SQLAlchemyError as e:
                db.session.rollback()
                return {'error': str(e)}, 403


class ProductsAPI(Resource):

    def get(self, product_id):
        product = Product.get_or_404(product_id)
        result = products_schema.dump(product).data
        return result

    def delete(self, product_id):
        product = Product.query.get_or_404(product_id)
        try:
            product.delete(product)
            response = make_response()
            response.status_code = 204
            return response

        except SQLAlchemyError as e:
                db.session.rollback()
                return {'error': str(e)}, 401

    def patch(self, product_id):
        product = Product.query.get_or_404(product_id)
        raw_dict = request.get_json(force=True)
        try:
            products_schema.validate(raw_dict, partial=True)
            product_dict = raw_dict['data']['attributes']
            for key, value in product_dict.items():
                setattr(product, key, value)

            product.update()
            return self.get(product_id)

        except ValidationError as err:
                return {'error': err.messages}, 401

        except SQLAlchemyError as e:
                db.session.rollback()
                return {'error': str(e)}, 401


api.add_resource(ProductsListAPI, '/')
api.add_resource(ProductsAPI, '/<product_id>')
