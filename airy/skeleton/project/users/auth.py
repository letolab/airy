from datetime import datetime
from hashlib import md5

from users.models import User, Session
from mongoengine.queryset import DoesNotExist


def login(user, raw_password, handler):
    session_key = md5(user.username + raw_password)
    handler.set_secure_cookie("session_key", session_key.hexdigest())

    session = Session.objects.get_or_create(user=user)[0]
    session.session_key = session_key.hexdigest()
    session.save()

    user.last_login = datetime.now()
    user.save()


def authenticate(password, username=None, email=None):
    try:
        if not email:
            user = User.objects.get(username=username)
        else:
            user = User.objects.get(email=email)
        if not user.check_password(password):
            return None
        return user
    except DoesNotExist:
        return None


def get_current_user(handler, *args, **kwargs):
    session_key = handler.get_secure_cookie("session_key")

    if not session_key:
        return None
    try:
        session = Session.objects.get(session_key=session_key)
        return session.user
    except DoesNotExist:
        return None
    return None
