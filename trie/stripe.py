import stripe

from trie import app

stripe.api_key = app.config['STRIPE_SECRET_KEY']
