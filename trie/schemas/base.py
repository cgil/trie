from marshmallow_jsonapi import Schema
from marshmallow import ValidationError


def not_empty(data):
    """Specify that data must not be empty."""
    if data is None:
        raise ValidationError('Data not provided.')


class BaseSchema(Schema):
    """Base schema."""

    def get_top_level_links(self, data, many):
        """Set self links."""
        if many:
            self_link = '/{}/'.format(self.Meta.type_)
        else:
            self_link = '/{}/{}'.format(self.Meta.type_, data['id'])
        return {'self': self_link}

    class Meta:
        strict = True
