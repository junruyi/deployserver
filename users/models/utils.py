from users.models import User


def init_model():
    if hasattr(User, 'init_account'):
        User.init_account()