"""
Bulk email script to automate sending first_contact emails.
There is one function to call `send` which takes in the name of the CSV file comtaining
apps to email.

Email templates should be stored at:
    `trie/templates/`

The app's to email CSV should be store at:
    `trie/scripts/assets/`

## Configuring the emailer
Set your email account's username and password in the appropriate
environment yaml file, ex:
```
# development.yaml
email:
    username:
    password:
    default_sender: # or a group under your account such as no-reply
```

## Sending emails using an app CSV:
```
# Prepare the app
$ cd trie
$ virtualenv env
$ source env/bin/activate
$ pip install fabric
$ fab bootstrap
$ fab shell
>> from trie.scripts.bulk_email import send
send('apps-games.csv')
```
"""


import csv
import os
import time

from tabulate import tabulate

from trie.lib import loggers
from trie.lib.mail import send_email
from trie.lib.templating import env

cwd = os.path.dirname(__file__)
logger = loggers.get_logger(__name__)

APP_NAME_KEY = 'app name'
CONTACT_EMAIL_KEY = 'contact email'
CONTACT_NAME_KEY = 'contact name'
FIRST_CONTACT_EMAIL_SENT_KEY = 'first contact email sent'
FIRST_CONTACT_EMAIL_TEMPLATE_NAME_KEY = 'first contact email template name'
APP_TOTE_STORE_URL = 'app tote store url'


def _get_csv_path(name):
    """Get the path to a CSV by name."""
    return os.path.join(cwd, 'output/app_info', name)


def _csv_to_dict(name):
    """Turns the CSV into a workable dictionary."""
    csv_path = _get_csv_path(name)
    result = []
    with open(csv_path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            result.append(row)
    return result


def _get_app_name(app):
    """Get the app's name."""
    return app[APP_NAME_KEY]


def _get_contact_first_name(app):
    """Get the contact's first name."""
    name = app.get(CONTACT_NAME_KEY)
    if name:
        return ' {}'.format(name.split(' ')[0])


def _get_contact_email(app):
    """Get the contacts email address."""
    return app[CONTACT_EMAIL_KEY]


def _get_email_subject(app_name):
    """Get the subject to send with the email."""
    return '{} <==> Tote'.format(app_name)


def _get_first_contact_email_template_name(app):
    """Get the email template name for the first contact email."""
    return app[FIRST_CONTACT_EMAIL_TEMPLATE_NAME_KEY]


def _get_app_tote_store_url(app):
    """Gets the tote store url for this app."""
    return app[APP_TOTE_STORE_URL]


def _did_send_first_contact_email(app):
    """Check if we already sent the first contact email."""
    first_contact = app[FIRST_CONTACT_EMAIL_SENT_KEY]
    if first_contact and first_contact.lower() == 'y':
        return True
    return False


def _print_summary(results):
    """Prints a summary of the results."""
    if not len(results) > 0:
        print 'No results to show in summary.'
        return

    table = {}
    for res in results:
        for k, v in res.iteritems():
            table.setdefault(k, []).append(v)
    print tabulate(table, headers='keys', tablefmt="simple")


def send(app_csv='apps.csv', verbose=True, dry_run=True):
    """
    Sends out emails to the apps in the provided csv.
    @param string app_csv: CSV name with apps to email. Stored in `trie/scripts/assets/`
    @param boolean verbose: If True, prints out a summary of the emails sent.
    @param dry_run boolean: If True, don't send emails, for debugging.
    """
    results = []
    app_info = _csv_to_dict(app_csv)
    for app in app_info:
        # Get all the app info needed for this request.
        app_name = _get_app_name(app)
        contact_first_name = _get_contact_first_name(app)
        email_address = _get_contact_email(app)
        app_tote_store_url = _get_app_tote_store_url(app)
        subject = _get_email_subject(app_name)

        # If we already sent the first contact email, continue.
        if _did_send_first_contact_email(app):
            result = dict(
                app_name=app_name,
                contact_first_name=contact_first_name,
                email_address=email_address,
                app_tote_store_url=app_tote_store_url,
                subject=subject,
                status='skipped',
                error=None,
            )
            logger.info(result)
            results.append(result)
            continue

        try:
            # Get the appropriate template to send.
            email_template = _get_first_contact_email_template_name(app)
            template = env.get_template(email_template)

            # Render the template with app info.
            content = template.render(
                app_name=app_name,
                contact_first_name=contact_first_name,
                app_tote_store_url=app_tote_store_url,
            )
            send_email(to=email_address, subject=subject, html=content, dry_run=dry_run)
            result = dict(
                app_name=app_name,
                contact_first_name=contact_first_name,
                email_address=email_address,
                app_tote_store_url=app_tote_store_url,
                subject=subject,
                status='success',
                error=None,
            )
        except Exception as e:
            result = dict(
                app_name=app_name,
                contact_first_name=contact_first_name,
                email_address=email_address,
                app_tote_store_url=app_tote_store_url,
                subject=subject,
                status='failure',
                error=str(e),
            )
        logger.info(result)
        results.append(result)

        # Sleep momentarily to avoid dos'ing the server.
        if not dry_run:
            time.sleep(0.1)
    if verbose:
        _print_summary(results)
