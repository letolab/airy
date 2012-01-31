Database
====================================

Airy currently supports MongoDB only. By default, it connects to the local MongoDB server
and uses the database specified in ``settings.database_name``.

Every app should define its models in ``models.py``. You may keep an empty ``models.py`` file if
your app doesn't need to store any data.

An ordinary ``models.py`` file may look like this:

.. code-block:: python

    from airy.core.db import *

    class Comment(Action):
        text = StringField(required=True)


    class Post(Document):
        title = StringField(max_length=128, required=True)
        text = StringField(required=True)
        is_published = BooleanField(default=False)
        comments = ListField(ReferenceField(Comment))

        def __unicode__(self):
            return self.title



It relies on `MongoEngine <http://mongoengine.org/>`_ for ORM.

Please refer to `MongoEngine Documentation <http://mongoengine.org/docs/>`_ for detailed documentation.

