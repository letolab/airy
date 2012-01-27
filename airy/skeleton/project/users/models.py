from datetime import datetime
from hashlib import md5

from airy.core.db import *


class Education(Document):
    university = StringField(max_length=512)
    degree = StringField(max_length=512)
    major = StringField(max_length=512)
    description = StringField(required=False)
    start_date = DateTimeField()
    end_date = DateTimeField()

    def __unicode__(self):
        return self.university


class Experience(Document):
    employer = StringField(max_length=512)
    position = StringField(max_length=512)
    description = StringField(required=False)
    start_date = DateTimeField()
    end_date = DateTimeField()

    def __unicode__(self):
        return self.employer


class Service(Document):
    name = StringField(max_length=512)
    date_created = DateTimeField(default=datetime.now)
    providers_num = IntField(default=0)

    def __unicode__(self):
        return self.name


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
    education = ListField(ReferenceField(Education))
    experience = ListField(ReferenceField(Experience))
    services = ListField(ReferenceField(Service))
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

    def delete_education(self, education_id):
        try:
            education = Education.objects.get(id=education_id)
            if education in self.education:
                self.update(pull__education=education)
                education.delete()
        except Exception:
            return

    def delete_service(self, service_id):
        try:
            service = Service.objects.get(id=service_id)
            if service in self.services:
                self.update(pull__services=service)
                service.providers_num -= 1
                service.save()
                if not service.providers_num:
                    service.delete()
        except Exception:
            return

    def delete_experience(self, experience_id):
        try:
            experience = Experience.objects.get(id=experience_id)
            if experience in self.experience:
                self.update(pull__experience=experience)
                experience.delete()
        except Exception:
            return

    def delete_recommended_book(self, book_id):
        try:
            recommended_book = Book.objects.get(id=book_id)
            if not recommended_book in self.recommended_books:
                return
            self.update(pull__recommended_books=recommended_book)
            recommended_book.delete()
        except Exception:
            return

    def delete_interest(self, interest_id):
        try:
            interest = Interest.objects.get(id=interest_id)
            if not interest in self.interests:
                return
            self.update(pull__interests=interest)
            interest.delete()
        except Exception:
            return


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
