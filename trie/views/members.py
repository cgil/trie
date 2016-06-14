from flask import Blueprint
from flask import request
from flask_restful import Api
from flask_security.utils import encrypt_password
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from trie.lib import loggers
from trie.lib.compress import compress
from trie.lib.database import db
from trie.lib.secure import authenticate
from trie.models.member import Member
from trie.schemas.members_schema import MembersSchema
from trie.views.base import BaseAPI
from trie.views.base import BaseListAPI


members_blueprint = Blueprint('members', __name__, url_prefix='/members')
api = Api(members_blueprint)

logger = loggers.get_logger(__name__)


class MembersListAPI(BaseListAPI):

    model = Member
    schema_model = MembersSchema

    @compress
    @authenticate
    def post(self):
        """Create a new record."""
        logger.info({
            'msg': 'Creating a new record.',
            'view': self.__class__.__name__,
            'method': 'post',
            'schema_model': self.schema_model.__name__,
            'model': self.model.__name__,
        })
        raw_dict = request.get_json(force=True)
        try:
            self.schema.validate(raw_dict)
            attrs = raw_dict['data'].get('attributes') or {}

            if 'password' in attrs:
                attrs['password'] = encrypt_password(attrs['password'])

            relationships = raw_dict['data'].get('relationships') or {}
            rel_attrs = {}
            for name, val in relationships.iteritems():
                rel_name = '{}_id'.format(name)
                rel_attrs[rel_name] = val['data']['id']
            attrs.update(rel_attrs)

            record = self.model(**attrs)
            record.update()
            query = self.model.get(record.id)
            result = self.schema.dump(query).data
            return result, 201

        except ValidationError as e:
                logger.error({
                    'msg': 'Error validating new record.',
                    'view': self.__class__.__name__,
                    'method': 'post',
                    'schema_model': self.schema_model.__name__,
                    'model': self.model.__name__,
                    'raw_dict': raw_dict,
                    'error': str(e)
                })
                return {'error': e.messages}, 403

        except SQLAlchemyError as e:
                logger.error({
                    'msg': 'Error creating new record.',
                    'view': self.__class__.__name__,
                    'method': 'post',
                    'schema_model': self.schema_model.__name__,
                    'model': self.model.__name__,
                    'raw_dict': raw_dict,
                    'error': str(e)
                })
                db.session.rollback()
                return {'error': str(e)}, 403


class MembersAPI(BaseAPI):

    model = Member
    schema_model = MembersSchema

    def patch(self, id):
        """Update one or more fields."""
        logger.info({
            'msg': 'Patching a record.',
            'view': self.__class__.__name__,
            'method': 'patch',
            'schema_model': self.schema_model.__name__,
            'model': self.model.__name__,
            'record_id': id,
        })
        record = self.model.get_or_404(id)
        raw_dict = request.get_json(force=True)
        try:
            self.schema.validate(raw_dict, partial=True)
            attrs = raw_dict['data'].get('attributes') or {}
            for key, value in attrs.items():
                if key == 'password':
                    value = encrypt_password(value)
                setattr(record, key, value)

            relationships = raw_dict['data'].get('relationships') or []
            if not isinstance(relationships, list):
                relationships = [relationships]
            for rel in relationships:
                record.update_relationship(rel['data']['type'], rel['data']['id'])

            record.update()
            record = self.model.get_or_404(id)
            result = self.schema.dump(record).data
            return result

        except ValidationError as e:
                logger.error({
                    'msg': 'Error validating patching a record.',
                    'view': self.__class__.__name__,
                    'method': 'patch',
                    'schema_model': self.schema_model.__name__,
                    'model': self.model.__name__,
                    'record_id': id,
                    'raw_dict': raw_dict,
                    'error': str(e),
                })
                return {'error': e.messages}, 401

        except SQLAlchemyError as e:
                logger.error({
                    'msg': 'Error patching a record.',
                    'view': self.__class__.__name__,
                    'method': 'patch',
                    'schema_model': self.schema_model.__name__,
                    'model': self.model.__name__,
                    'record_id': id,
                    'raw_dict': raw_dict,
                    'error': str(e),
                })
                db.session.rollback()
                return {'error': str(e)}, 401


api.add_resource(MembersListAPI, '/')
api.add_resource(MembersAPI, '/<id>')
