"Configuration"
import tornado.options
from tornado.options import define, options
import os

define("port", default=8000, help="Run on the given port", type=int)
define("secret", default='', help="Application secret")
define("template_path", default="./templates", help="Template directory path")
define("static_path", default="./static", help="Static directory path")
define("app_title", default="Example Web App", help="Default app title")
define("xsrf_cookies", default=True, help="Disable XSRF cookies")
define("installed_apps", default=[], help="List of installed applications", multiple=True)

class Settings:
    def __init__(self, **entries):
        self.__dict__.update(entries)

settings = Settings()

def _preconfigure(project_root, config_filename='settings.py', argv=[]):
    "Read config file, process command-line args"
    tornado.options.parse_command_line(argv)
    tornado.options.parse_config_file(config_filename)

    dsettings = {}
    for key in options:
        dsettings[key] = getattr(options, key)

    if options.template_path == './templates':
        dsettings['template_path'] = os.path.join(project_root, './templates')
    if options.static_path == './static':
        dsettings['static_path'] = os.path.join(project_root, './static')

    config = __import__('settings')
    for name in dir(config):
        if not name.startswith('_'):
            dsettings[name] = getattr(config, name)

    settings.__dict__.update(**dsettings)

    return dsettings


