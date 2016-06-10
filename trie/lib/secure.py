import functools

from flask import request
from flask.ext.security.decorators import auth_token_required
from flask.ext.security import Security

from trie.lib import loggers
from trie.utils.configuration import config

security = Security()

logger = loggers.get_logger(__name__)


def _is_internal():
    """Check if this is an internal call."""
    allowed_internal_auth_keys = config.get('security.internal_auth_keys')
    allowed_internal_auth_tokens = config.get('security.internal_auth_tokens')
    for k, v in allowed_internal_auth_keys.iteritems():
        header_token = request.headers.get(v)
        if (
            header_token is not None and
            header_token == allowed_internal_auth_tokens.get(k)
        ):
            return True
    return False


def authenticate(fn=None, **auth_kwargs):
    # Called with optional arguments.
    if fn is None:
        return functools.partial(authenticate, **auth_kwargs)

    # Called with no optional arguments.
    @functools.wraps(fn)
    def decorated(*args, **kwargs):
        logger.info({
            'msg': 'Authenticating incoming request',
            'args': args,
            'kwargs': kwargs,
            'headers': request.headers.to_list(),
            'params': request.query_string,
        })
        # Authenticate
        auth_res = auth_token_required(fn)(*args, **kwargs)
        successfully_authenticated = isinstance(auth_res, dict)
        logger.info({
            'msg': 'Authentication response',
            'args': args,
            'kwargs': kwargs,
            'headers': request.headers.to_list(),
            'params': request.query_string,
            'auth_success': successfully_authenticated,
        })
        return auth_res
    return decorated
