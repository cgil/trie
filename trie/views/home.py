from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask.ext.login import login_required
from flask.ext.login import login_user
from sqlalchemy.exc import IntegrityError

from trie import db
from trie.forms.account_form import AccountForm
from trie.lib.compress import compress
from trie.models.member import Member

home = Blueprint('home', __name__, template_folder='trie/templates')


def handle_authenticated_member(member):
    """Handle the authenticated member after logging in."""
    login_user(member)
    return redirect(url_for('home.loggedin'))


@home.route('/', methods=['GET', 'POST'])
@compress
def index():
    form = AccountForm(request.form)
    if form.validate_on_submit():
        if form.login.data:
            known_member = Member.get_known_member(form.email.data, form.password.data)
            if known_member:
                return handle_authenticated_member(known_member)
            form.password.errors.append('email or password is incorrect')
        elif form.signup.data:
            if not Member.email_exists(form.email.data):
                known_member = Member(
                    form.email.data,
                    form.password.data
                )
                db.session.add(known_member)
                try:
                    db.session.commit()
                except IntegrityError:
                    # TODO: Log failure
                    db.session.rollback()
                    form.password.errors.appen('email or password is incorrect')
                    return render_template('teaser.html', form=form)
                return handle_authenticated_member(known_member)
            form.email.errors.append('an account already exists with that email')
    return render_template('teaser.html', form=form)


@home.route('/loggedin')
@login_required
def loggedin():
    return render_template('loggedin.html')


@home.route('/contact')
def contact():
    return render_template('contact.html')


@home.route('/new')
def new_landing_page():
    return render_template('new.html')
