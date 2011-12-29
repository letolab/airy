"Base engine"
import tornado.web
from tornado import template, autoreload
from tornadio2 import SocketServer, TornadioRouter
from airy.core.conf import settings, _preconfigure
from airy.core import web
import logging
import sys
import os

AIRY_ROOT = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../')

from pprint import pprint

def execute(project_root, argv):
    _preconfigure(project_root, argv=argv[1:])

    if len(argv) <= 1:
        print 'Please provide a command.'
    elif argv[1] == 'run':
        run(project_root)
    elif argv[1] == 'shell':
        shell()
    else:
        print 'Unrecognised command.'


def shell():
    from IPython import embed
    embed()

def run(project_root):
    serverurls = []
    servermodels = []

    # add Airy static file handler
    serverurls.extend([
        (r"/airy/(.*)", tornado.web.StaticFileHandler, {"path": os.path.join(AIRY_ROOT, 'static')})
    ])

    # add AIry core handler
    serverurls.extend(web.core_router.urls)

    # add application handlers
    for appname in settings.installed_apps:
        # add app urls
        appurls = __import__('%s.urls' % appname, fromlist=['%s.url'%appname])
        urlpatterns = getattr(appurls, 'urlpatterns')
        serverurls.extend(urlpatterns)
        try:
            models = __import__('%s.models' % appname, fromlist=['%s.models'%appname])
            servermodels.append(models)
        except ImportError:
            pass

    # restart on code change
    for root,dirs,files in os.walk(settings.template_path):
        for x in files:
            if os.path.splitext(x)[1].lower() == '.html': # track templates
                autoreload._watched_files.add(os.path.join(root,x))

    application = tornado.web.Application(serverurls, **settings.__dict__)
    settings.application = web.site.application = application
    web.site.loader = template.Loader(settings.template_path)
    
    SocketServer(application)

