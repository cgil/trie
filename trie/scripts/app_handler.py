from os import listdir
import csv
import os

from trie.utils import io


cwd = os.path.dirname(__file__)

APP_INFO_PATH = os.path.join(cwd, 'output/app_info')
FILTERED_OUTPUT_FILE_PATH = os.path.join(cwd, 'output/app_handler', 'clean_apps.json')
FINAL_APP_INFO_PATH = os.path.join(cwd, 'output/email_collection')
OUTPUT_CSV_PATH = os.path.join(cwd, 'output/app_info')


def filter_only_usable_apps():
    """Filters all the apps from different categories into one usable list."""
    good_apps = {}
    for bundle in _get_app_bundles():
        for app in bundle.get('apps', []):
            app_id = app['app_id']
            if app_id not in good_apps:
                if app['publisher_site']:
                    good_apps[app_id] = app

    io.write_json_to_file(dict(apps=good_apps.values()), FILTERED_OUTPUT_FILE_PATH)


def create_csv_from_apps(file_name, csv_name='apps.csv'):
    """Turns the output of the apps blob into csv format."""
    file_path = os.path.join(FINAL_APP_INFO_PATH, file_name)
    apps = io.get_json_from_file(file_path).get('apps', {})
    csv_path = os.path.join(OUTPUT_CSV_PATH, csv_name)
    if len(apps) > 0:
        keys = apps[0].keys()
        keys.append('contacted')
        with open(csv_path, 'wb') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            for app in apps:
                encoded_app = {}
                app['contacted'] = False
                for k, v in app.iteritems():
                    # Don't include unprocessed apps with no collected emails.
                    if not app.get('email_collection_processed', False):
                        continue
                    try:
                        encoded_app[k] = v.encode('utf-8')
                    except AttributeError:
                        encoded_app[k] = v
                dict_writer.writerow(encoded_app)


def _get_app_bundles():
    """Get bundles of apps."""
    files = [
        f for f in listdir(APP_INFO_PATH)
        if os.path.isfile(os.path.join(APP_INFO_PATH, f))
        and f.endswith('.json')
    ]
    for file_name in files:
        file_path = os.path.join(APP_INFO_PATH, file_name)
        yield io.get_json_from_file(file_path)
