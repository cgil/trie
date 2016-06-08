from trie.models.role import Role
from trie.tests import factories
from trie.tests.base import CRUDTestCase


class RoleTestCase(CRUDTestCase):

    def setUp(self):
        super(RoleTestCase, self).setUp()
        self.model_factory = factories.RoleFactory
        self.model = Role
        self.url_prefix = 'roles'

    def test_crud(self):
        """Test roles CRUD."""
        self._test_crud()
