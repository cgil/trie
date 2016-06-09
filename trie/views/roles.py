from flask import Blueprint
from flask_restful import Api

from trie.lib import loggers
from trie.lib.secure import authenticate
from trie.models.role import Role
from trie.schemas.roles_schema import RolesSchema
from trie.views.base import BaseAPI
from trie.views.base import BaseListAPI


roles_blueprint = Blueprint('roles', __name__, url_prefix='/roles')
api = Api(roles_blueprint)

logger = loggers.get_logger(__name__)


class RolesListAPI(BaseListAPI):

    model = Role
    schema_model = RolesSchema

    @authenticate(allow='all')
    def post(self):
        return super(RolesListAPI, self).post()


class RolesAPI(BaseAPI):

    model = Role
    schema_model = RolesSchema

api.add_resource(RolesListAPI, '/')
api.add_resource(RolesAPI, '/<id>')
