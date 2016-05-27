from marshmallow_jsonapi import Schema
from marshmallow import ValidationError


def not_empty(data):
    """Specify that data must not be empty."""
    if data is None:
        raise ValidationError('Data not provided.')


class BaseSchema(Schema):
    """Base schema."""

    class Meta:
        strict = True
