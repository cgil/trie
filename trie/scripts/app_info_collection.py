"""
Script to collect app info from the itunes RSS Feed
    https://itunes.apple.com/us/genre/ios/id36?mt=8

There are two functions that can be called.
`collect` takes in a genre and feed type pair and outputs a .json file with the app info.
`bulk_collect` takes in a list of genres and feed types and outputs several .json files.

## Feed Type
A type of ranking feed for apps. Such as top paid apps, or top grossing apps.

# Genre
A category genre that apps may belong to. Such as business, or lifestyle.


## Output
All output is located at `trie/scripts/output/app_info/`

## Quickstart
```
$ cd trie
$ virtualenv env
$ source env/bin/activate
$ pip install fabric
$ fab bootstrap
$ fab shell
>> from trie.scripts import app_info_collection

# Collect one pair.
>> app_info_collection.collect('top_fee_applications', 'lifestyle', limit=300)

# Collect everything.
>> app_info_collection.bulk_collect(limit=300)
```
"""


import datetime
import os
import requests
import time

import tldextract

from trie.lib import loggers
from trie.utils import io
from trie.utils.convert import camel_case_to_snake_case


cwd = os.path.dirname(__file__)
logger = loggers.get_logger(__name__)

BASE_URL = 'https://itunes.apple.com/us/rss/{}/limit={}/genre={}/json'
FEED_TYPES = {
    'top_free_applications': 'topfreeapplications',
    'new_free_applications': 'newfreeapplications',
    'top_grossing_applications': 'topgrossingapplications',
    'top_paid_applications': 'toppaidapplications',
    'new_paid_applications': 'newpaidapplications',
    'new_applications': 'newapplications',
}

GENRES = {
    'books': 6018,
    'business': 6000,
    'catalogs': 6022,
    'education': 6017,
    'finance': 6015,
    'food_and_drink': 6023,
    'games': 6014,
    'health_and_fitness': 6013,
    'lifestyle': 6012,
    'magazine_and_newspapers': 6021,
    'medical': 6020,
    'music': 6011,
    'navigation': 6010,
    'news': 6009,
    'photo_and_video': 6008,
    'productivity': 6007,
    'reference': 6006,
    'shopping': 6024,
    'social_networking': 6005,
    'sports': 6004,
    'travel': 6003,
    'utilities': 6002,
    'weather': 6001,
}


def _get_output_path(name):
    """Get the path to the output file."""
    return os.path.join(cwd, 'output/app_info', name)


def _get_publisher_name(entry):
    """Get the publishers name - usually company name."""
    return entry['im:artist']['label']


def _get_publisher_site(entry):
    """Gets the website for the publisher of the app."""
    bundle_id = entry['id']['attributes']['im:bundleId']  # com.site.app_name
    url = '.'.join(bundle_id.split('.')[::-1])
    parsed = tldextract.extract(url)
    if parsed.domain and parsed.suffix:
        return '{}.{}'.format(parsed.domain, parsed.suffix)


def _get_alternative_app_name(entry):
    """Gets an alternative app name to compare against."""
    bundle_id = entry['id']['attributes']['im:bundleId']  # com.site.app_name
    url = '.'.join(bundle_id.split('.')[::-1])
    parsed = tldextract.extract(url)
    if parsed.subdomain:
        return parsed.subdomain
    return parsed.domain


def _get_app_category(entry):
    """Get the apps listed category."""
    return entry['category']['attributes']['term']


def _get_app_name(entry):
    """Get the apps name."""
    return entry['im:name']['label']


def _get_app_id(entry):
    """Get the itunes app id."""
    return entry['id']['attributes']['im:id']


def collect(feed_type_key, genre_key, limit=20, output_file_name=None):
    """
    Collect app info for one feed type genre combination.
    @param string feed_type_key: The key to the app feed type.
    @param string genre_key: The key to the app genre.
    @param int limit: How many items to collect - max 200.
    @param output_file_name: Name of the output json file. Should end with a .json extension.
    """

    feed_type = FEED_TYPES[feed_type_key]
    url = BASE_URL.format(
        feed_type,
        limit,
        GENRES[genre_key],
    )
    apps = []
    try:
        res = requests.get(url)
        data = res.json()
    except Exception as e:
        logger.error(dict(
            msg='Error requesting app data',
            feed_type_key=feed_type_key,
            genre_key=genre_key,
            url=url,
            limit=limit,
            error=e,
        ))
        return

    entries = data['feed']['entry']
    for entry in entries:
        try:
            publisher_name = _get_publisher_name(entry)
            publisher_site = _get_publisher_site(entry)
            app_category = _get_app_category(entry)
            app_name = _get_app_name(entry)
            alternative_app_name = _get_alternative_app_name(entry)
            app_id = _get_app_id(entry)
            app = dict(
                publisher_name=publisher_name,
                publisher_site=publisher_site,
                app_category=app_category,
                app_name=app_name,
                alternative_app_name=alternative_app_name,
                app_id=app_id,
            )
            apps.append(app)
        except Exception as e:
            logger.error(dict(
                msg='Error parsing app info',
                feed_type_key=feed_type_key,
                genre_key=genre_key,
                error=e,
            ))

    if len(apps) > 0:
        if not output_file_name:
            output_file_name = camel_case_to_snake_case(
                '{}__{}__{}.json'.format(
                    feed_type_key,
                    genre_key,
                    datetime.date.today(),
                )
            )
        output_file = _get_output_path(output_file_name)
        apps = dict(apps=apps)

        io.write_json_to_file(apps, output_file)
        logger.info('Finished collecting data for feed_type_type: {}, genre_key: {}'.format(
            feed_type_key,
            genre_key,
        ))


def bulk_collect(feed_type_keys=None, genre_keys=None, limit=200):
    """
    Does a bulk collection of apps accross several genres.
    @param list feed_type_key: Key to app feed types.
    @param list genre_keys: Keys to app genres.
    @param int limit: How many items to collect per genre/feed_type pair - max 200.
    """
    if not feed_type_keys:
        feed_type_keys = FEED_TYPES.keys()
    if not genre_keys:
        genre_keys = GENRES.keys()

    for feed_type_key in feed_type_keys:
        for genre_key in genre_keys:
            collect(
                feed_type_key,
                genre_key,
                limit=limit,
            )
            time.sleep(0.2)
    logger.info(dict(
        msg='Finished bulk collection',
        genre_keys=genre_keys,
        feed_type_keys=feed_type_keys,
        limit=limit,
    ))
