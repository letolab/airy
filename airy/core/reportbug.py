from airy.core.conf import settings
from airy.core.mail import mail_admins

def report_on_fail(function):

    def wrapped(ins, *args, **kwargs):
        try:
            return function(ins, *args, **kwargs)
        except:
            if settings.debug:
                raise
            ReportBug(ins, args=args, kwargs=kwargs)

    wrapped.__doc__ = function.__doc__
    wrapped.__name__ = function.__name__

    return wrapped


def ReportBug(handler=None, args=[], kwargs={}):

    import sys
    import traceback
    import os

    # Mail the admins with the error
    exc_info = sys.exc_info()

    message = u'\n\nargs:\n %s\n\nkwargs:\n%s\n\n' % (args, kwargs)
    message += u'%s\n\n' % ('\n'.join(traceback.format_exception(*exc_info)),)

    exp = sys.exc_info()

    subject = str(exp[1]).strip()
    text_content = message
    mail_admins(subject, text_content)

