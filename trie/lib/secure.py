import functools

from flask import request
from flask.ext.security.decorators import auth_token_required
from flask.ext.security import Security

from trie.utils.configuration import config

security = Security()


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
        if 'allow' in auth_kwargs and auth_kwargs['allow'] == 'all':
            return fn(*args, **kwargs)
        # Bypass auth if internal call.
        if _is_internal():
            return fn(*args, **kwargs)
        # Authenticate
        return auth_token_required(fn)(*args, **kwargs)
    return decorated
