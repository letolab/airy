import smtplib
import thread
import urllib
import urlparse
from datetime import datetime, timedelta
from email.mime.text import MIMEText

from airy.core.web import AiryHandler, AiryRequestHandler
from airy.core.conf import settings

from users.decorators import login_required
from users.forms import *
from users.models import PasswordResetToken


class IndexHandler(AiryRequestHandler):

    def get(self):
        self.render("page.html")


class HomeHandler(AiryHandler):

    def get(self):
        if not self.current_user:
            self.render("#menu", "users/user_out_menu.html")
            self.render("#content", "index.html")
            return
        user = self.get_current_user()
        self.render("#menu", "users/user_in_menu.html")
        self.render("#content", "index.html")

    def post(self):
        if self.current_user:
            self.redirect("/")
            return
        form = RegistrationForm(self.get_flat_arguments())
        if form.is_valid():
            user = form.save(self)
            self.redirect("/")
        else:
            self.render("#menu", "users/user_out_menu.html")
            self.render("#content", "index.html", form=form)


class AccountsLoginHandler(AiryHandler):
    def get(self):
        if self.get_current_user():
            self.redirect("/")
        else:
            form = LoginForm()
            self.render("#content", "users/login.html", form=form)

    def post(self):
        form = LoginForm(self.get_flat_arguments())
        if form.is_valid():
            form.save(self)
            self.redirect("/")
        else:
            self.render("#content", "users/login.html", form=form)


class AccountsLogoutHandler(AiryHandler):
    def get(self):
        self.clear_cookie("session_key")
        self.render("#menu", "users/user_out_menu.html")
        self.redirect("/")


class AccountsRegisterHandler(AiryHandler):
    def get(self):
        form = RegistrationForm()
        self.render("#content", "users/register.html", form=form)

    def post(self):
        form = RegistrationForm(self.get_flat_arguments())
        if form.is_valid():
            user = form.save(self)
            self.redirect("/")
        else:
            self.render("#content", "users/register.html", form=form)


class AccountsProfileHandler(AiryHandler):
    @login_required
    def get(self):
        user = self.get_current_user()
        self.render(
            "#content", "users/profile/main.html",
        )


class AccountsForeignProfileHandler(AiryHandler):
    def get(self, object_id):
        try:
            companies = list()
            try:
                user = User.objects.get(id=object_id)
            except:
                user = User.objects.get(username=object_id)
            self.render(
                "#content", "users/profile/foreign_profile.html",
                user=user, companies=companies, current_user=self.get_current_user()
            )
        except:
            self.render("#content", "http_404.html")


class AccountsChangeUserInfoHandler(AiryHandler):
    @login_required
    def post(self):
        field = self.get_argument('field')
        value = self.get_argument('value')
        user = self.get_current_user()
        setattr(user, field, value)
        user.save()


class AccountsProfileDeleteHandler(AiryHandler):
    @login_required
    def post(self):
        user = self.get_current_user()
        actions = {
            'education': user.delete_education,
            'services': user.delete_service,
            'experience': user.delete_experience,
            'recommended_book': user.delete_recommended_book,
            'interests': user.delete_interest,
        }

        actions[self.get_argument('field')](self.get_argument('object_id'))


class FileUpload(AiryHandler):
    @login_required
    def get(self, action):
        if action == 'upload':
            form = FileUploadForm()
            self.render(
                "#profile-picture",
                "users/profile/picture_upload.html",
                form=form
            )
            self.execute('project.users.picture_init();')
        else:
            self.render("#profile-picture", "users/profile/picture.html")

    @login_required
    def post(self, *args, **kwargs):
        form = FileUploadForm(self.get_flat_arguments(), self.get_files())
        if form.is_valid():
            form.save(self.get_current_user())
            self.render("#profile-picture", "users/profile/picture.html")
            self.render("#menu", "user_in_menu.html")
            return
        self.render(
            "#profile-picture",
            "users/profile/picture_upload.html",
            form=form
        )


class AccountsRecoverPasswordHandler(AiryHandler):
    def get(self, path=None):
        if not path:
            form = PasswordRecoveryForm()
            self.render("#content", "users/password_recovery/recovery.html", form=form)
            return

        args = urlparse.parse_qs(path)
        if not self.token_is_valid(args.get('token', [None])[0]):
            self.redirect("/users/recovery/")

        form = NewPasswordForm()
        self.render("#content", "users/password_recovery/new_password.html", form=form)

    def token_is_valid(self, token):
        try:
            password_reset_token = PasswordResetToken.objects.get(token=token)
            if datetime.now() > password_reset_token.expired:
                return False
            return True
        except Exception:
            return False

    def get_items_from_path(self, path):
        try:
            args = urlparse.parse_qs(path)
            password_reset_token = PasswordResetToken.objects.get(token=args['token'][0])
            user = User.objects.get(password_reset_token_list__contains=password_reset_token)
            return user, password_reset_token
        except Exception:
            return None, None

    def post(self, path=None):
        #Email or username for password recovery, send mail
        if not path:
            form = PasswordRecoveryForm(self.get_flat_arguments())
            if form.is_valid():
                user = form.save()
                thread.start_new_thread(self.send_recovery_mail, (user, self.generate_recovery_link(user)))
                self.render("#content", "users/password_recovery/password_reset_sent.html")
            else:
                self.render("#content", "users/password_recovery/recovery.html", form=form)
            return

        #New password and confirmation
        form = NewPasswordForm(self.get_flat_arguments())

        user, password_reset_token = self.get_items_from_path(path)

        if form.is_valid():
            form.save(self, user)

            #Delete password reset token
            user.update(pull__password_reset_token_list=password_reset_token)
            password_reset_token.delete()

            self.redirect('/')
        else:
            self.render("#content", "users/password_recovery/new_password.html", form=form)


    def generate_recovery_link(self, user):
        expired = datetime.now() + timedelta(days=1)
        token = md5(str(user.id) + expired.strftime("%H:%M:%S %m/%d/%Y")).hexdigest()

        password_reset_token = PasswordResetToken(expired=expired, token=token)
        password_reset_token.save()

        user.password_reset_token_list.append(password_reset_token)
        user.save()

        params = urllib.urlencode(dict(token=token))
        return 'http://%s:%s/users/recovery/%s' % (HOST, PORT, params)

    def send_recovery_mail(self, user, url):
        smtp_server = self.connect_smtp_server(
            settings.email_host,
            settings.email_port,
            settings.email_host_user,
            settings.email_host_password
        )
        smtp_server.sendmail(
            settings.email_host_user,
            user.email,
            self.build_message(user, url)
        )
        smtp_server.quit()

    def build_message(self, user, url):
        msg = MIMEText('Password recovery link: %s' % url)
        msg['Subject'] = 'Password recovery'
        return msg.as_string()

    def connect_smtp_server(self, email_host, email_port, user, password):
        smtp_server = smtplib.SMTP('%s:%s' % (email_host, email_port))
        smtp_server.starttls()
        smtp_server.login(user, password)
        return smtp_server
