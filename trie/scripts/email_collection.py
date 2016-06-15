import datetime
import json
import os

import clearbit

from trie.lib import loggers
from trie.utils import io

cwd = os.path.dirname(__file__)
logger = loggers.get_logger(__name__)

API_KEYS = None
API_KEYS_FILE_NAME = 'clearbit_api_keys.json'
OUTPUT_DIR = 'output/email_collection'


class APIError(Exception):
    """API Error."""


def _get_json_from_file(file_path):
    """Gets json from a file."""
    with open(file_path, 'r') as infile:
        data = json.load(infile)
    return data


def _get_output_path(name):
    """Get the path to a CSV by name."""
    return os.path.join(cwd, OUTPUT_DIR, name)


def _get_app_info_data_file_path(file_name):
    """Gets the app info file path for the given file name."""
    return os.path.join(cwd, 'output/app_info/', file_name)


def _load_clearbit_api_keys():
    """Load the clearbit api keys."""
    global API_KEYS
    if not API_KEYS:
        file_path = os.path.join(cwd, 'assets/{}'.format(API_KEYS_FILE_NAME))
        API_KEYS = _get_json_from_file(file_path).get('keys', {})


def _get_apps(file_name):
    """Gets the app info from a json file."""
    file_path = _get_app_info_data_file_path(file_name)
    return _get_json_from_file(file_path)


def _get_clearbit(api_type):
    """
    Gets a clearbit instance for the given api_type.
    @param string api_type: `prospector` or `company`.
    """
    global API_KEYS

    if not API_KEYS:
        raise APIError('No API Keys found.')

    for api_key in API_KEYS:
        if not API_KEYS[api_key].get(api_type):
            clearbit.key = api_key
            return clearbit

    raise APIError('No remaining valid API Keys.')


def _invalidate_clearbit_api_key(api_key, api_type):
    """Invalidates an api key for an api type."""
    global API_KEYS
    API_KEYS[api_key][api_type] = str(datetime.datetime.utcnow())
    file_path = os.path.join(cwd, 'assets/{}'.format(API_KEYS_FILE_NAME))
    io.write_json_to_file(API_KEYS, file_path)


def _make_contact_request(domain, seniority=None, titles=None, role=None, limit=1, email='false'):
    """Make a request to get contacts."""
    while True:
        try:
            # Attempt to make an api request.
            _clearbit = _get_clearbit('prospector')
            res = _clearbit.Prospector.search(
                domain=domain,
                seniority=seniority,
                titles=titles,
                role=role,
                limit=limit,
                email=email,
            ) or []

            try:
                res = list(res)
            except TypeError:
                # No results.
                res = []

            return res
        except APIError:
            # No API keys left.
            raise
        except Exception as e:
            logger.error(dict(
                msg='Error getting contacts',
                domain=domain,
                clearbit_api_key=_clearbit.key,
                error=e,
            ))
            if e.response.status_code == 401:
                # Unauthorized. Current API key is spent for this api type.
                _invalidate_clearbit_api_key(_clearbit.key, 'prospector')
            else:
                # Something else went terribly wrong skip.
                return []


def _make_company_request(domain, dry_run=True):
    """Make a request to get a company"""
    while True:
        try:
            _clearbit = _get_clearbit('company')
            # Attempt to make an api request.
            res = _clearbit.Company.find(
                domain=domain,
            ) or {}

            return dict(res)
        except APIError:
            # No API keys left.
            raise
        except Exception as e:
            # Current API key is spent for this api type.
            logger.error(dict(
                msg='Error getting a company',
                domain=domain,
                clearbit_api_key=_clearbit.key,
                error=e,
            ))
            if e.response.status_code == 401:
                _invalidate_clearbit_api_key(_clearbit.key, 'company')
            else:
                # Something else went terribly wrong.
                return {}


def _get_company(app, dry_run=True):
    """Gets the company info for the given app."""
    company = _make_company_request(app['publisher_site'], dry_run=dry_run)
    if 'pending' in company:
        company = {}

    res = {}
    res['company_name'] = company.get('name')
    res['company_phone_numbers'] = company.get('site', {}).get('phoneNumbers')
    res['company_email_addresses'] = company.get('site', {}).get('emailAddresses')
    res['company_location'] = company.get('location')
    res['company_metrics'] = company.get('metrics')
    res['company_facebook'] = company.get('facebook', {}).get('handle')
    res['company_linkedin'] = company.get('linkedin', {}).get('handle')
    res['company_twitter'] = company.get('twitter', {}).get('handle')
    return res


def _get_contacts(app, dry_run=True):
    """Get company contacts."""
    email = 'false' if dry_run else 'true'

    # Attempt to get the ceo.
    people = _make_contact_request(
        app['publisher_site'],
        role='ceo',
        email=email,
    )
    if not people:
        # Attempt to get founders.
        people = _make_contact_request(
            app['publisher_site'],
            role='founder',
            email=email,
        )
    if not people:
        # Attempt to get executives.
        people = _make_contact_request(
            app['publisher_site'],
            seniority='executive',
            email=email,
        )
    if not people:
        # Attempt to get directors.
        people = _make_contact_request(
            app['publisher_site'],
            seniority='director',
            email=email,
        )
    if not people:
        # Attempt to get managers.
        people = _make_contact_request(
            app['publisher_site'],
            seniority='manager',
            email=email,
        )
    if not people:
        # Attempt to get anyone.
        people = _make_contact_request(
            app['publisher_site'],
            email=email,
        )
    contacts = []
    for person in people:
        person = dict(person)
        contact = dict(
            full_name=person.get('name', {}).get('fullName'),
            given_name=person.get('name', {}).get('givenName'),
            family_name=person.get('name', {}).get('familyName'),
            title=person.get('title'),
            email=person.get('email'),
        )
        contacts.append(contact)
    return contacts


def collect(
        file_name,
        start_index=0,
        end_index=None,
        dry_run=True
):
    """Suppliments the app info with email and company info """
    apps = _get_apps(file_name)
    _load_clearbit_api_keys()

    index = 0
    for index, app in enumerate(apps.get('apps', [])):
        import ipdb
        ipdb.set_trace()
        # Continue until we get to the given start index.
        if start_index > index:
            continue

        # Stop if we pass the end index.
        if end_index is not None and index > end_index:
            break

        try:
            contacts = _get_contacts(app, dry_run=dry_run)
            company = _get_company(app, dry_run=dry_run)
        except APIError:
            logger.info(dict(
                msg='Pausing due to API Error. Need more api keys.',
                last_app=app,
                file_name=file_name,
                index=index,
                next_command_to_run='collect({}, start_index={})'.format(
                    file_name,
                    index,
                )
            ))
            break
        app['contacts'] = contacts
        app['company'] = company
        last_index = index

    file_name = '{}-{}__{}'.format(start_index, last_index, file_name)
    output_path = _get_output_path(file_name)
    io.write_json_to_file(apps, output_path)
