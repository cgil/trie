from trie.models.role import Role
from trie.tests.base import BaseTestCase


class RoleTestCase(BaseTestCase):

    def test_role(self):
        """Test that we can initiate a role."""
        attrs = dict(
            name='awesome-role',
            description='super awesome role',
        )
        role = Role(**attrs)
        role.save(role)
        res = Role.get(role.id)
        for attr in attrs:
            assert getattr(res, attr) == attrs[attr]
