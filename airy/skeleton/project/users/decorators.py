from airy.core.conf import settings
from projects.models import Project
from mongoengine.queryset import DoesNotExist

from users.auth import get_current_user

def login_required(function):

    def wrapped(handler, *args, **kwargs):
        if get_current_user(handler):
            return function(handler, *args, **kwargs)
        else:
            handler.redirect(getattr(settings, 'login_url', '/accounts/login'))

    wrapped.__doc__ = function.__doc__
    wrapped.__name__ = function.__name__

    return wrapped


def is_project_manager(function):

    def wrapped(handler, project_id, *args, **kwargs):
        try:
            project = Project.objects.get(id=project_id)
        except DoesNotExist:
            handler.redirect('/')
        else:
            user = get_current_user(handler)
            if user in project.managers:
                return function(handler, project_id, *args, **kwargs)
            else:
                # TODO: change on permission denied page
                handler.redirect('/')

    return wrapped


def is_participant(function):

    def wrapped(handler, project_id, *args, **kwargs):
        try:
            project = Project.objects.get(id=project_id)
        except DoesNotExist:
            handler.redirect('/')
        else:
            user = get_current_user(handler)
            if user in project.managers or user in project.participants:
                return function(handler, project_id, *args, **kwargs)
            else:
                # TODO: change on permission denied page
                handler.redirect('/')

    return wrapped
