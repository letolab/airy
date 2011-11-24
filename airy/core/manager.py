"Base engine"
import tornado.web
import tornado.ioloop
import tornado.options
from tornado.options import define, options
import monitor
import os

define("port", default=8000, help="Run on the given port", type=int)
define("secret", default='', help="Application secret")
define("template_path", default="./templates", help="Template directory path")
define("static_path", default="./static", help="Static directory path")
define("app_title", default="Example Web App", help="Default app title")
define("xsrf_cookies", default=True, help="Disable XSRF cookies")
define("installed_apps", default=[], help="List of installed applications", multiple=True)

def _preconfigure(project_root):
    settings = {}
    for key in options:
        settings[key] = getattr(options, key)

    if options.template_path == './templates':
        settings['template_path'] = os.path.join(project_root, './templates')
    if options.static_path == './static':
        settings['static_path'] = os.path.join(project_root, './static')
    return settings


def execute(project_root, argv):
    tornado.options.parse_command_line()
    tornado.options.parse_config_file('settings.py')

    if len(argv) <= 1:
        print 'Please provide a command.'
    elif argv[1] == 'run':
        run(project_root)
    else:
        print 'Unrecognised command.'


def run(project_root):
    serverurls = []
    for appname in options.installed_apps:
        appurls = __import__('%s.urls' % appname, fromlist=['%s.url'%appname])
        serverurls.extend(getattr(appurls, 'urlpatterns'))

    settings = _preconfigure(project_root)
    
    # restart on code change
    monitor.start(interval=5.0) # check every 5 second
    for root,dirs,files in os.walk(settings['template_path']):
        for x in files:
            if os.path.splitext(x)[1].lower() == '.html': # track templates
                monitor.track(os.path.join(root,x))
    
    application = tornado.web.Application(serverurls, **settings)
    application.listen(options.port)

    print '---\nStarting server on port %d...' % options.port
    
    tornado.ioloop.IOLoop.instance().start()

