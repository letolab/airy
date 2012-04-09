from airy.core.conf import settings
from airy.core.mail import mail_admins

def report_on_fail(function):

    def wrapped(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except:
            if settings.debug:
                raise
            ReportBug()

    wrapped.__doc__ = function.__doc__
    wrapped.__name__ = function.__name__

    return wrapped


def ReportBug(handler=None):

    import sys
    import traceback
    import os

    # Mail the admins with the error
    exc_info = sys.exc_info()

    if exc_info:
        _file, _line, _func, _line = traceback.extract_tb(exc_info[2])[0]
        _file = os.path.basename(_file)

    else:
        _file, _line, _func, _line = (None, None, None, None)

    message = 'Exception in %s (line %s)' % (
        _file,
        _line
        )
    message += 'Traceback:\n%s\n\n' % ('\n'.join(traceback.format_exception(*exc_info)),)

    exp = sys.exc_info()

    subject = str(exp[1])
    text_content = message
    mail_admins(subject, text_content)

