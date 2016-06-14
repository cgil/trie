from flask import Blueprint
from flask import request
from flask_restful import Api
from flask_restful import Resource

from trie.lib import loggers
from trie.lib.compress import compress
from trie.models.member import Member
from trie.utils.configuration import config


auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')
api = Api(auth_blueprint)

logger = loggers.get_logger(__name__)


class AuthAPI(Resource):

    @compress
    def post(self):
        """Authenicate the user."""
        logger.info({
            'msg': 'Getting authentication details for a member.',
            'view': self.__class__.__name__,
            'method': 'post',
        })
        raw_dict = request.get_json(force=True)
        member = Member.get_if_authenticates(
            raw_dict['email'],
            raw_dict['password'],
        )
        if member:
            return {
                'message': 'success',
                'auth_token': member.get_auth_token(),
                'auth_token_header': config.get('security.token_authentication_header'),
                'expires_in_seconds': config.get('security.token_max_age'),
            }, 200
        return {'message': 'Cannot authenticate you.'}, 403

api.add_resource(AuthAPI, '/')
