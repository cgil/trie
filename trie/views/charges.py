from decimal import Decimal
import uuid

from flask import Blueprint
from flask import request
from flask_restful import Api
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError

from trie.lib import loggers
from trie.lib.checkout import stripe
from trie.lib.database import db
from trie.lib.sendgrid import sendgrid
from trie.models.member import Member
from trie.models.order import Order
from trie.models.order_item import OrderItem
from trie.models.product import Product
from trie.utils.configuration import config

logger = loggers.get_logger(__name__)

charges_blueprint = Blueprint('charges', __name__, url_prefix='/charges')
api = Api(charges_blueprint)


class ChargesListAPI(Resource):

    def post(self):
        """Create a new charge."""
        logger.info({
            'msg': 'Starting a new charge.',
            'view': 'ChargesListAPI',
            'method': 'post',
        })
        raw_dict = request.get_json(force=True)
        logger.info({
            'msg': 'Charge with data.',
            'raw_dict': raw_dict,
            'view': 'ChargesListAPI',
            'method': 'post',
        })
        try:
            stripe_customer = stripe.Customer.create(
                email=raw_dict['token']['email'],
                card=raw_dict['token']['id'],
            )
        except Exception as e:
            logger.error({
                'msg': 'Error creating Stripe Customer.',
                'error': str(e),
                'view': 'ChargesListAPI',
                'method': 'post',
            })
            return {'error': str(e)}, 403

        member = Member.get_by_email(raw_dict['token']['email'])
        # Create a member if one doesn't exist.
        if member:
            logger.info({
                'msg': 'Member found, updating record..',
                'member_email': raw_dict['token']['email'],
                'stripe_customer_id': stripe_customer.id,
                'view': 'ChargesListAPI',
                'method': 'post',
            })
            member.stripe_customer_id = stripe_customer.id
            member.save(member)
        else:
            logger.info({
                'msg': 'No member found, creating a new member.',
                'member_email': raw_dict['token']['email'],
                'view': 'ChargesListAPI',
                'method': 'post',
            })
            temp_password = str(uuid.uuid4())[:8]
            try:
                member = Member(
                    email=raw_dict['token']['email'],
                    password=temp_password,
                    stripe_customer_id=stripe_customer.id,
                )
                member.save(member)
            except SQLAlchemyError as e:
                    logger.error({
                        'msg': 'Error creating member.',
                        'error': str(e),
                        'view': 'ChargesListAPI',
                        'method': 'post',
                    })
                    db.session.rollback()
                    return {'error': str(e)}, 403

        logger.info({
            'msg': 'Creating a new order.',
            'member_id': member.id,
            'view': 'ChargesListAPI',
            'method': 'post',
        })
        # Create a new order for the member.
        try:
            addresses = raw_dict['addresses']
            order = Order(
                member_id=member.id,
                store_id=raw_dict['storeId'],
                financial_status='pending',
                total_price=0,
                shipping_address_city=addresses['shipping_address_city'],
                shipping_address_country=addresses['shipping_address_country'],
                shipping_address_country_code=addresses['shipping_address_country_code'],
                shipping_address_1=addresses['shipping_address_line1'],
                shipping_address_zip=addresses['shipping_address_zip'],
                shipping_name=addresses['shipping_name'],
            )
            db.session.add(order)
            db.session.flush()
        except Exception as e:
            logger.error({
                'msg': 'Error creating a new order.',
                'member_id': member.id,
                'error': str(e),
                'view': 'ChargesListAPI',
                'method': 'post',
            })
            return {'error': str(e)}, 403

        logger.info({
            'msg': 'Creating order items.',
            'view': 'ChargesListAPI',
            'method': 'post',
        })
        # Get all products in the order.
        basket = raw_dict['basket']
        order_items = []
        total_price = Decimal(0)
        for item in basket:
            product = Product.get(item['id'])
            if not product:
                logger.error({
                    'msg': 'Product not found.',
                    'product': item,
                    'view': 'ChargesListAPI',
                    'method': 'post',
                })
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

        logger.info({
            'msg': 'Charging member.',
            'member_id': member.id,
            'order_id': order.id,
            'total_price': total_price,
            'stripe_customer_id': member.stripe_customer_id,
            'view': 'ChargesListAPI',
            'method': 'post',
        })
        # Charge the member.
        try:
            stripe.Charge.create(
                customer=member.stripe_customer_id,
                amount=int(total_price * 100),  # amount in cents, again
                currency='usd',
                description='Tote Store - purchased items.',
                metadata={
                    'order_id': order.id
                }
            )
        except (stripe.error.CardError, stripe.error.InvalidRequestError) as e:
            logger.error({
                'msg': 'Stripe error.',
                'member_id': member.id,
                'order_id': order.id,
                'total_price': total_price,
                'error': str(e),
                'view': 'ChargesListAPI',
                'method': 'post',
            })
            # The card has been declined
            db.session.rollback()
            return {'error': str(e)}, 403

        # Store the order and order items.
        order.financial_status = 'paid'
        order.total_price = Decimal(total_price)
        db.session.add(order)
        for order_item in order_items:
            db.session.add(order_item)

        logger.info({
            'msg': 'Finalizing order.',
            'member_id': member.id,
            'order_id': order.id,
            'total_price': total_price,
            'view': 'ChargesListAPI',
            'method': 'post',
        })
        # Finalize all transactions.
        try:
            db.session.commit()
        except SQLAlchemyError as e:
                logger.error({
                    'msg': 'Error finalizing order.',
                    'member_id': member.id,
                    'order_id': order.id,
                    'error': str(e),
                    'view': 'ChargesListAPI',
                    'method': 'post',
                })
                db.session.rollback()
                return {'error': str(e)}, 403

        try:
            logger.info({
                'msg': 'Sending confirmation email to member.',
                'member_id': member.id,
                'to_email': member.email,
                'from_email': config.get('sendgrd.default_from'),
                'order_id': order.id,
                'total_price': total_price,
                'view': 'ChargesListAPI',
                'method': 'post',
            })
            # Send a confirmation email.
            sendgrid.send_email(
                from_email=config.get('sendgrid.default_from'),
                to=[{'email': member.email}],
                subject='Tote Store - Purchase Confirmation.',
                text=(
                    'Thank you for your purchase! Order id: {}, total: ${}.'
                    'For support contact us at support@totestore.com '.format(
                        order.id, total_price)
                ),
            )
        except Exception:
            logger.error({
                'msg': 'Failed to send confirmation email to member.',
                'member_id': member.id,
                'to_email': config.get('sendgrid.internal_new_order_to'),
                'from_email': config.get('sendgrid.default_from'),
                'order_id': order.id,
                'total_price': total_price,
                'view': 'ChargesListAPI',
                'method': 'post',
            })

        try:
            logger.info({
                'msg': 'Sending new order email internally.',
                'member_id': member.id,
                'to_email': config.get('sendgrid.internal_new_order_to'),
                'from_email': config.get('sendgrid.default_from'),
                'order_id': order.id,
                'total_price': total_price,
                'view': 'ChargesListAPI',
                'method': 'post',
            })
            # Send email a reminder email to ourselves about this order.
            sendgrid.send_email(
                from_email=config.get('sendgrid.default_from'),
                to=[{'email': config.get('sendgrid.internal_new_order_to')}],
                subject='New Order!',
                text=(
                    'New Order! order_id: {}, member_id={}, store_id={}, total: ${}'.format(
                        order.id, member.id, order.store_id, total_price)
                ),
            )
        except Exception:
            logger.error({
                'msg': 'Failed to send new order email internally.',
                'member_id': member.id,
                'to_email': config.get('sendgrid.internal_new_order_to'),
                'from_email': config.get('sendgrid.default_from'),
                'order_id': order.id,
                'total_price': total_price,
                'view': 'ChargesListAPI',
                'method': 'post',
            })

        logger.info({
            'msg': 'Successfully finished processing a new charge.',
            'member_id': member.id,
            'order_id': order.id,
            'store_id': order.store_id,
            'total_price': total_price,
            'view': 'ChargesListAPI',
            'method': 'post',
        })

        return {}, 201


api.add_resource(ChargesListAPI, '/')
