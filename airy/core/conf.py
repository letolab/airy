"""
Configuring Airy projects.

By default Airy parses ``settings.py`` file located in the project's directory.

You may specify parameters either in the file or on command line when launching your
project, for example:

.. code-block:: console

    $ python manage.py runserver --port=80

Most commonly used options:

* port (default=8000)

    Run on the given port

* host (default="127.0.0.1:8000")

    Bind to the given ip/port.

* template_path (default="./templates")

    Path to the directory containing project templates.

* static_path (default="./static")

    Path to your project's static files (Airy will serve it automatically on /static/)

For a full list of options, see ``python manage.py help``

"""
import tornado.options
from tornado.options import define, options
import os

define("port", default=8000, help="Run on the given port", type=int)
define("flash_policy_port", default=8043, help="Port to run Flash policy on (for older browsers)", type=int)
define("flash_policy_file", default="./flashpolicy.xml", help="Flash policy file")
define("secret", default='', help="Application secret")
define("template_path", default="./templates", help="Template directory path")
define("static_path", default="./static", help="Static directory path")
define("app_title", default="Example Web App", help="Default app title")
define("xsrf_cookies", default=True, help="Disable XSRF cookies")
define("installed_apps", default=[], help="List of installed applications", multiple=True)
define("host", default="127.0.0.1:8000")
define("email_host", default="smtp.gmail.com")
define("email_port", default=587)
define("email_host_user", default="")
define("email_host_password", default="")


class Settings(object):
    def __init__(self, **entries):
        self.__dict__.update(entries)

    def __getattribute__(self, name):
        return object.__getattribute__(self, name.lower())
        

settings = Settings()

def _ensure_defaults(dsettings, options, project_root, config_filename):

    # paths    
    if options.template_path == './templates':
        dsettings['template_path'] = os.path.join(project_root, 'templates')
    if options.static_path == './static':
        dsettings['static_path'] = os.path.join(project_root, 'static')
    if options.flash_policy_file == './flashpolicy.xml':
        dsettings['flash_policy_file'] = os.path.join(project_root, 'flashpolicy.xml')
    dsettings['locale_paths'] = ()

    # translation
    dsettings['use_i18n'] = True
    dsettings['use_l10n'] = True
    dsettings['language_code'] = 'en-us'

    # settings
    dsettings['settings_module'] = config_filename.replace('/', '.')[:-3].strip('.')

    # formats
    dsettings['datetime_format'] = getattr(options, 'datetime_format', 'N j, Y, P')
    dsettings['time_format'] = getattr(options, 'time_format', 'P')

    return dsettings

def _preconfigure(project_root, config_filename='settings.py', argv=[]):
    "Read config file, process command-line args"
    tornado.options.parse_command_line(argv)
    tornado.options.parse_config_file(config_filename)

    dsettings = {}
    for key in options:
        dsettings[key] = getattr(options, key)
    
    _ensure_defaults(dsettings, options, project_root, config_filename)

    config = __import__('settings')
    for name in dir(config):
        if not name.startswith('_'):
            dsettings[name] = getattr(config, name)

    settings.__dict__.update(**dsettings)
    
    settings.socket_io_port = settings.port

    return dsettings


