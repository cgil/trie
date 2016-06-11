from flask_mail import Mail
from flask_mail import Message


mailer = Mail()


def send_email(to=None, body=None, html=None, subject=None, dry_run=False):
    if dry_run:
        return

    msg = Message(
        recipients=[to],
        body=body,
        html=html,
        subject=subject,
    )
    mailer.send(msg)
