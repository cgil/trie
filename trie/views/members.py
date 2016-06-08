from flask import Blueprint
from flask_restful import Api

from trie.models.member import Member
from trie.schemas.members_schema import MembersSchema
from trie.views.base import BaseAPI
from trie.views.base import BaseListAPI


members_blueprint = Blueprint('members', __name__, url_prefix='/members')
api = Api(members_blueprint)


class MembersListAPI(BaseListAPI):

    model = Member
    schema_model = MembersSchema


class MembersAPI(BaseAPI):

    model = Member
    schema_model = MembersSchema


api.add_resource(MembersListAPI, '/')
api.add_resource(MembersAPI, '/<id>')
