"Project settings"

debug = True

database_name = 'airydb' # replace with your Mongo DB name

installed_apps = [
    'users',
]

template_context_processors = [
    'airy.core.context_processors.markup',
    'users.context_processors.settings',
    'users.context_processors.user',
]

login_url = '/accounts/login'

cookie_secret = 'airy_secret' # replace with yours

authentication_backends = [
    'users.auth',
]

datetime_input_formats = (
    '%Y-%m-%d %H:%M:%S',     # '2006-10-25 14:30:59'
    '%Y-%m-%d %H:%M',        # '2006-10-25 14:30'
    '%Y-%m-%d',              # '2006-10-25'
    '%m/%d/%Y %H:%M:%S',     # '10/25/2006 14:30:59'
    '%m/%d/%Y %H:%M',        # '10/25/2006 14:30'
    '%m/%d/%Y',              # '10/25/2006'
    '%m/%d/%y %H:%M:%S',     # '10/25/06 14:30:59'
    '%m/%d/%y %H:%M',        # '10/25/06 14:30'
    '%m/%d/%y',              # '10/25/06'
)

email_host = 'smtp.gmail.com'
email_host_user = ''
email_host_password = ''
email_port = 587
