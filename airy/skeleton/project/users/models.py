from datetime import datetime
from hashlib import md5

from airy.core.db import *


class PasswordResetToken(Document):
    expired = DateTimeField()
    token = StringField(max_length=128)


class User(Document):
    username = StringField(max_length=30)
    password = StringField(max_length=128)
    first_name = StringField(max_length=30)
    last_name = StringField(max_length=30)
    email = StringField(max_length=30)
    last_login = DateTimeField(default=datetime.now)
    date_joined = DateTimeField(default=datetime.now)
    picture_url = StringField(max_length=512, default='')
    picture_height = IntField(default=0)
    picture_width = IntField(default=0)
    headline = StringField(max_length=512, default='')
    country = StringField(max_length=512, required=False)
    state = StringField(max_length=512, required=False)
    city = StringField(max_length=512, required=False)
    bio = StringField(default='')
    contact = StringField(default='')
    other_sites = StringField(default='')
    interests = ListField(ReferenceField("Tag"))
    recommended_books = ListField(ReferenceField("Book"))
    password_reset_token_list = ListField(ReferenceField(PasswordResetToken))
    rating = IntField(default=0)

    def __unicode__(self):
        if self.first_name and self.last_name:
            return u'%s %s' % (self.first_name, self.last_name)
        return u'%s' % self.username

    def get_picture_url(self):
        if self.picture:
            return self.picture.url
        return getattr(settings, 'DEFAULT_PICTURE_URL',
            '/static/images/profile-default.png')

    def check_password(self, raw_password):
        if self.password == md5(raw_password).hexdigest():
            return True
        return False

    def set_password(self, raw_password):
        self.password = md5(raw_password).hexdigest()


class Session(Document):
    user = ReferenceField(User)
    session_key = StringField(max_length=64)


class Tag(Document):
    tag = StringField(max_length=64)


class Interest(Tag):
    pass


class Book(Document):
    text = StringField(max_length=1024)
    ref = URLField(required=False)
