from datetime import datetime
from md5 import md5
from airy import forms
from airy.core.conf import settings
from os.path import join

from users.auth import authenticate, login
from users.models import User, Session


class RegistrationForm(forms.Form):
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput(render_value=True))
    password2 = forms.CharField(widget=forms.PasswordInput(render_value=True), label='Confirm password')

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).count() > 0:
            raise forms.ValidationError('A user with such email is already registered')
        return self.cleaned_data['email']

    def clean(self, *args, **kwargs):
        super(RegistrationForm, self).clean(*args, **kwargs)
        if 'password' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password'] != self.cleaned_data['password2']:
                self._errors['password'] = [u'Passwords must match.']
                self._errors['password2'] = [u'Passwords must match']
        return self.cleaned_data

    def save(self, obj):
        user = User(
            username=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
            education=[],
            experience=[],
            services=[]
        )
        user.set_password(self.cleaned_data['password'])
        user.save()

        user = authenticate(username=self.cleaned_data['email'], password=self.cleaned_data['password'])

        session_key = md5(self.cleaned_data['username'] + self.cleaned_data['password'])
        obj.set_secure_cookie("session_key", session_key.hexdigest())
        session = Session.objects.get_or_create(user = user)[0]
        session.session_key = session_key.hexdigest()
        session.save()

        return user


class LoginForm(forms.Form):
    username = forms.CharField(label="E-mail")
    password = forms.CharField(widget=forms.PasswordInput(render_value=True))

    def clean(self):
        if 'username' in self.cleaned_data and 'password' in self.cleaned_data:
            username = self.cleaned_data['username']
            if not '@' in username:
                user = authenticate(username=username, password=self.cleaned_data['password'])
            else:
                user = authenticate(email=username, password=self.cleaned_data['password'])
            if not user:
                raise forms.ValidationError('Email or password are incorrect')
        else:
            return None

        self.user = user
        return user

    def save(self, handler):
        login(self.user, self.cleaned_data['password'], handler)
        return self.user


class FileUploadForm(forms.Form):
    picture = forms.FileField(label='Choose a file')

    def save(self, user=None, *args, **kwargs):
        file = open(join(settings.static_path, 'media', self.cleaned_data['picture'].name), 'wb')
        file.write(self.cleaned_data['picture'].read())
        file.close()
        if user:
            user.picture_url = '/static/media/%s' % self.cleaned_data['picture'].name
            user.save()
        return '/static/media/%s' % self.cleaned_data['picture'].name


class PasswordRecoveryForm(forms.Form):
    email_or_login = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'large input-text'}),
        label='Please enter your email or password'
    )

    def clean_email_or_login(self):
        data = self.cleaned_data['email_or_login']
        try:
            if '@' in data:
                self.user = User.objects.get(email=data)
            else:
                self.user = User.objects.get(username=data)
        except Exception as e:
            raise forms.ValidationError('A user with such email or username does not exist')
        return self.cleaned_data['email_or_login']

    def save(self):
        return self.user


class NewPasswordForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(render_value=True),
        label='Please enter new password'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(render_value=True),
        label='Confirm password'
    )

    def clean(self, *args, **kwargs):
        super(NewPasswordForm, self).clean(*args, **kwargs)
        if 'password' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password'] != self.cleaned_data['password2']:
                self._errors['password'] = [u'Passwords must match.']
                self._errors['password2'] = [u'Passwords must match']
        return self.cleaned_data

    def save(self, handler, user):
        user.set_password(self.cleaned_data['password'])
        user.save()
        login(user, self.cleaned_data['password'], handler)
        return user