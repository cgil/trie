from flask import make_response
from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from querystring_parser import parser
from sqlalchemy.exc import SQLAlchemyError

from trie.lib import loggers
from trie.lib.database import db
from trie.lib.secure import authenticate

logger = loggers.get_logger(__name__)


def format_params(obj):
    """Formats the params dictionary."""
    # Turns comma separated values into arrays.
    for k in obj:
        if isinstance(obj[k], dict):
            format_params(obj[k])
        else:
            obj[k] = obj[k].split(',')


def parse_query_string(query_string):
    """Parses the query string."""
    query_params = parser.parse(query_string)
    format_params(query_params)
    return query_params


class BaseListAPI(Resource):

    # The Queryable API model.
    model = None
    # Response model schema
    schema_model = None

    @property
    def schema(self):
        """Get an instance of a schema model."""
        return self.schema_model()

    @authenticate
    def get(self):
        """Get all records."""
        logger.info({
            'msg': 'Getting all records.',
            'view': self.__class__.__name__,
            'method': 'get',
            'schema_model': self.schema_model.__name__,
            'model': self.model.__name__,
        })
        records = self.model.query.filter(self.model.deleted_at.is_(None)).all()
        results = self.schema.dump(records, many=True).data
        return results

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
            relationships = raw_dict['data'].get('relationships') or {}
            rel_attrs = {}
            for name, val in relationships.iteritems():
                rel_name = '{}_id'.format(name)
                rel_attrs[rel_name] = val['data']['id']
            attrs.update(rel_attrs)

            record = self.model(**attrs)
            record.save(record)
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


class BaseAPI(Resource):

    # The Queryable API model.
    model = None
    # Response model schema
    schema_model = None

    @property
    def schema(self):
        """Get an instance of a schema model."""
        return self.schema_model()

    @authenticate
    def get(self, id):
        """Get a single record."""
        logger.info({
            'msg': 'Getting a record.',
            'view': self.__class__.__name__,
            'method': 'get',
            'schema_model': self.schema_model.__name__,
            'model': self.model.__name__,
            'record_id': id,
        })
        record = self.model.get_or_404(id)
        result = self.schema.dump(record).data
        return result

    @authenticate
    def delete(self, id):
        """Delete a record."""
        logger.info({
            'msg': 'Deleting a record.',
            'view': self.__class__.__name__,
            'method': 'delete',
            'schema_model': self.schema_model.__name__,
            'model': self.model.__name__,
            'record_id': id,
        })
        record = self.model.get_or_404(id)
        try:
            record.delete(record)
            response = make_response()
            response.status_code = 204
            return response

        except SQLAlchemyError as e:
                logger.error({
                    'msg': 'Error deleting a record.',
                    'view': self.__class__.__name__,
                    'method': 'delete',
                    'schema_model': self.schema_model.__name__,
                    'model': self.model.__name__,
                    'record_id': id,
                    'error': str(e),
                })
                db.session.rollback()
                return {'error': str(e)}, 401

    @authenticate
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
                setattr(record, key, value)

            relationships = raw_dict['data'].get('relationships') or []
            if not isinstance(relationships, list):
                relationships = [relationships]
            for rel in relationships:
                record.update_relationship(rel['data']['type'], rel['data']['id'])

            record.update()
            return self.get(id)

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
