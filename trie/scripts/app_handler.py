import os
from os import listdir

from trie.utils import io


cwd = os.path.dirname(__file__)

APP_INFO_PATH = os.path.join(cwd, 'output/app_info')
FILTERED_OUTPUT_FILE_PATH = os.path.join(cwd, 'output/app_handler', 'clean_apps.json')


def filter_only_usable_apps():
    """Filters all the apps from different categories into one usable list."""
    good_apps = {}
    for bundle in get_app_bundles():
        for app in bundle.get('apps', []):
            app_id = app['app_id']
            if app_id not in good_apps:
                if app['publisher_site']:
                    good_apps[app_id] = app

    io.write_json_to_file(dict(apps=good_apps.values()), FILTERED_OUTPUT_FILE_PATH)


def get_app_bundles():
    """Get bundles of apps."""
    files = [
        f for f in listdir(APP_INFO_PATH)
        if os.path.isfile(os.path.join(APP_INFO_PATH, f))
        and f.endswith('.json')
    ]
    for file_name in files:
        file_path = os.path.join(APP_INFO_PATH, file_name)
        yield io.get_json_from_file(file_path)
