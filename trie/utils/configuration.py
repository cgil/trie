import os
import yaml


class Configuration(object):
    """Loads a yaml configuration file."""

    def __init__(self):
        self.config = self.load()

    def _get(self, key_components):
        """Low-level method to look up a key in a dictionary."""
        value = self.config
        for k in key_components:
            value = value[k]
        return value

    def get(self, key, default=None):
        """Get the configuration for a specific variable, using dots as
        delimiters for nested objects.

        :param key: Key in the config to lookup
        :type key: str
        :param default: Default value to return if key is not in the config.
        :type default: str
        """
        key_components = key.split('.')
        try:
            return self._get(key_components)
        except KeyError:
            return default

    def load(self):
        """Loads the configuration file."""
        env_path = os.environ.get('CONFIG_ENV') or 'config/development.yaml'
        if not os.path.exists(env_path):
            raise Exception('{0} does not exist'.format(env_path))

        stream = open(env_path, 'r')
        return yaml.safe_load(stream)


config = Configuration()
