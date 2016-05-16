from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from sqlalchemy.exc import IntegrityError

from trie import db
from trie.forms.account_form import AccountForm
from trie.models.member import Member

home = Blueprint('home', __name__, template_folder='trie/templates')


@home.route('/', methods=['GET', 'POST'])
def index():
    form = AccountForm(request.form)
    if form.validate_on_submit():
        if form.login.data:
            if Member.does_authenticate(form.email.data, form.password.data):
                return redirect(url_for('home.loggedin'))
        elif form.signup.data:
            if not Member.email_exists(form.email.data):
                member = Member(
                    form.email.data,
                    form.password.data
                )
                db.session.add(member)
                try:
                    db.session.commit()
                except IntegrityError:
                    # TODO: Log failure
                    db.session.rollback()
                    return render_template('index.html', form=form)
        return redirect(url_for('home.loggedin'))
    return render_template('index.html', form=form)


@home.route('/loggedin')
def loggedin():
    return render_template('loggedin.html')
