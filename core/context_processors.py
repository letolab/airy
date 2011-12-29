from tornado.escape import to_unicode

class Markup(object):
    @staticmethod
    def linebreaks(text):
        return to_unicode(text).replace('\n', '<br />')

def markup(handler, **kwargs):
    return {'markup': Markup()}

