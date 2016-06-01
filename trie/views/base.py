from flask import make_response
from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from trie import db


class BaseListAPI(Resource):

    # The Queryable API model.
    model = None
    # Response model schema
    schema_model = None

    @property
    def schema(self):
        """Get an instance of a schema model."""
        return self.schema_model()

    def get(self):
        """Get all records."""
        records = self.model.query.filter(self.model.deleted_at.is_(None)).all()
        results = self.schema.dump(records, many=True).data
        return results

    def post(self):
        """Create a new record."""
        raw_dict = request.get_json(force=True)
        try:
            self.schema.validate(raw_dict)
            attrs = raw_dict['data']['attributes']
            record = self.model(**attrs)
            record.save(record)
            query = self.model.get(record.id)
            result = self.schema.dump(query).data
            return result, 201

        except ValidationError as err:
                return {'error': err.messages}, 403

        except SQLAlchemyError as e:
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

    def get(self, id):
        """Get a single record."""
        record = self.model.get_or_404(id)
        result = self.schema.dump(record).data
        return result

    def delete(self, id):
        """Delete a record."""
        record = self.model.get_or_404(id)
        try:
            record.delete(record)
            response = make_response()
            response.status_code = 204
            return response

        except SQLAlchemyError as e:
                db.session.rollback()
                return {'error': str(e)}, 401

    def patch(self, id):
        record = self.model.get_or_404(id)
        raw_dict = request.get_json(force=True)
        try:
            self.schema.validate(raw_dict, partial=True)
            attrs = raw_dict['data']['attributes']
            for key, value in attrs.items():
                setattr(record, key, value)

            record.update()
            return self.get(id)

        except ValidationError as err:
                return {'error': err.messages}, 401

        except SQLAlchemyError as e:
                db.session.rollback()
                return {'error': str(e)}, 401
