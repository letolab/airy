from handlers import *

urlpatterns = [
    (r"/.*", IndexHandler), # root handler to accept old-style HTTP requests

    (r"/", HomeHandler),
    (r"/accounts/login", AccountsLoginHandler),
    (r"/accounts/logout", AccountsLogoutHandler),
    (r"/accounts/profile", AccountsProfileHandler),
    (r"/accounts/profile/change/", AccountsChangeUserInfoHandler),
    (r"/accounts/profile/delete/", AccountsProfileDeleteHandler),
    (r"/accounts/profile/(?P<object_id>[^\/]+)", AccountsForeignProfileHandler),
    (r"/accounts/profile/picture/(?P<action>\w+)", FileUpload),
    (r"/accounts/recovery/(?P<path>.+)?", AccountsRecoverPasswordHandler),
    (r"/accounts/register", AccountsRegisterHandler),

    # Username handler
    (r"/u/(?P<object_id>\w+)", AccountsForeignProfileHandler),
]


