from airy.core.conf import settings as asettings

def settings(handler, **kwargs):
    return {'settings': asettings}

def user(handler, **kwargs):
    return {'user': handler.get_current_user()}
