from airy.core.conf import settings
from mongoengine.queryset import DoesNotExist
from users.auth import get_current_user

def login_required(function):

    def wrapped(handler, *args, **kwargs):
        if get_current_user(handler):
            return function(handler, *args, **kwargs)
        else:
            handler.redirect(getattr(settings, 'login_url', '/accounts/login'))

    wrapped.__doc__ = function.__doc__
    wrapped.__name__ = function.__name__

    return wrapped
