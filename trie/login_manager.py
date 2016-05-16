from flask.ext.login import LoginManager
from trie.models.member import Member


login_manager = LoginManager()


@login_manager.user_loader
def load_member(member_id):
    return Member.get(member_id).first()
