"Base engine"
import tornado.web
import tornado.ioloop
from airy.core.conf import settings, _preconfigure
import monitor
import os

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
    for appname in settings.installed_apps:
        appurls = __import__('%s.urls' % appname, fromlist=['%s.url'%appname])
        models = __import__('%s.models' % appname, fromlist=['%s.models'%appname])
        serverurls.extend(getattr(appurls, 'urlpatterns'))
        servermodels.append(models)

    # restart on code change
    monitor.start(interval=5.0) # check every 5 second
    for root,dirs,files in os.walk(settings.template_path):
        for x in files:
            if os.path.splitext(x)[1].lower() == '.html': # track templates
                monitor.track(os.path.join(root,x))
    
    application = tornado.web.Application(serverurls, **settings.__dict__)
    application.listen(settings.port)

    print '---\nStarting server on port %d...' % settings.port
    
    tornado.ioloop.IOLoop.instance().start()

