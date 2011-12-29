from airy.core.conf import settings
from mongoengine import *

connect(getattr(settings, 'database_name', 'airy'))

