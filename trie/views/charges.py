from decimal import Decimal
import uuid

from flask import Blueprint
from flask import request
from flask_restful import Api
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError

from trie import db
from trie import stripe
from trie.models.member import Member
from trie.models.order import Order
from trie.models.order_item import OrderItem
from trie.models.product import Product


charges_blueprint = Blueprint('charges', __name__, url_prefix='/charges')
api = Api(charges_blueprint)


class ChargesListAPI(Resource):

    def post(self):
        """Create a new charge."""
        raw_dict = request.get_json(force=True)
        stripe_customer = stripe.Customer.create(
            email=raw_dict['token']['email'],
            card=raw_dict['token']['id'],
        )
        member = Member.get_by_email(raw_dict['token']['email'])
        # Create a member if one doesn't exist.
        if not member:
            temp_password = str(uuid.uuid4())[:8]
            try:
                member = Member(
                    email=raw_dict['token']['email'],
                    password=temp_password,
                    stripe_customer_id=stripe_customer.id,
                )
                member.save(member)
            except SQLAlchemyError as e:
                    db.session.rollback()
                    return {'error': str(e)}, 403

        # Create a new order for the member.
        order = Order(
            member_id=member.id,
            store_id=raw_dict['storeId'],
            financial_status='pending',
            total_price=0,
            shipping_address_city=raw_dict['addresses']['shipping_address_city'],
            shipping_address_country=raw_dict['addresses']['shipping_address_country'],
            shipping_address_country_code=raw_dict['addresses']['shipping_address_country_code'],
            shipping_address_1=raw_dict['addresses']['shipping_address_line1'],
            shipping_address_zip=raw_dict['addresses']['shipping_address_zip'],
            shipping_name=raw_dict['addresses']['shipping_name'],
        )
        db.session.add(order)
        db.session.flush()

        # Get all products in the order.
        basket = raw_dict['basket']
        order_items = []
        total_price = Decimal(0)
        for item in basket:
            product = Product.get(item['id'])
            if not product:
                return {'error': 'Product not found: {}.'.format(item['id'])}, 404

            order_items.append(
                OrderItem(
                    member_id=member.id,
                    store_id=raw_dict['storeId'],
                    product_id=product.id,
                    order_id=order.id,
                    quantity=item['_quantity'],
                )
            )
            total_price += product.price * item['_quantity']

        # Charge the member.
        try:
            stripe.Charge.create(
                customer=member.stripe_customer_id,
                amount=total_price * 100,  # amount in cents, again
                currency='usd',
                description='Tote Store - purchased items.',
                metadata={
                    'order_id': order.id
                }
            )
        except stripe.error.CardError as e:
            # The card has been declined
            db.session.rollback()
            return {'error': str(e)}, 403

        # Store the order and order items.
        order.financial_status = 'paid'
        order.total_price = Decimal(total_price)
        db.session.add(order)
        for order_item in order_items:
            db.session.add(order_item)


        import ipdb
        ipdb.set_trace()
        # Finalize all transactions.
        db.session.commit()

        # Send a confirmation email.
        return {}, 201

api.add_resource(ChargesListAPI, '/')
