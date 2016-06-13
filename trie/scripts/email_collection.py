import json
import os
import requests

from trie.lib import loggers

cwd = os.path.dirname(__file__)
logger = loggers.get_logger(__name__)


def _build_api_url(domain):
    """Builds the api url."""
    # Email Hunter
    return 'https://emailhunter.co/trial/v1/search?offset=0&domain={}&format=json'.format(
        domain,
    )


def _get_app_info_data_file_path(file_name):
    """Gets the app info file path for the given file name."""
    return os.path.join(cwd, 'output/app_info/', file_name)


def _get_app_info_json(file_name):
    """Gets the app info from a json file."""
    file_path = _get_app_info_data_file_path(file_name)
    with open(file_path, 'r') as infile:
        data = json.load(infile)
    return data


def _get_contact_name(email):
    """Get the contact name from the email."""
    pass


def _get_contact_info(app):
    """Gets the contact info for the given app."""
    app_domain = app['publisher_site']
    url = _build_api_url(app_domain)
    res = requests.get(url)
    data = res.json()
    contacts = []
    for email in data['emails']:
        contact_name = _get_contact_name(email)
        contact = dict(
            email=email['value'],
            email_type=email['type'],
            confidence=email['confidence'],
            pattern=email['pattern'],
            contact_name=contact_name,

        )
        contacts.append(contact)
    return contacts


def collect(file_name):
    apps = _get_app_info_json(file_name)
    for app in apps:
        contacts = _get_contact_info(app)
        app['contacts'] = contacts
