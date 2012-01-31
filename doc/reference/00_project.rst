Project Structure
====================================

A typical Airy project has the following structure:

.. code-block:: none

    myproject/
        myapp/
            __init__.py
            handlers.py
            models.py
            urls.py
        static/
        templates/
        __init__.py
        flashpolicy.xml
        manage.py
        requirements.pip
        settings.py

Airy expects every app enabled in ``settings.installed_apps`` to have at least those 4 files under ``myapp/`` from above.

* ``myapp/handlers.py``

    A file containing all your handlers for ``myapp``.
    It may also have a 'root' handler subclassing :py:class:`~airy.core.web.AiryRequestHandler`

* ``myapp/models.py``

    Your database models go here. See :doc:`Database <02_database>` for more details.

* ``myapp/urls.py``

    Define URLs for your app there. For example a typical file may look like this:

    .. code-block:: python

        # snippet from users/urls.py:

        from handlers import *

        urlpatterns = [
            (r"/.*", IndexHandler), # root handler to accept old-style HTTP requests

            (r"/", HomeHandler),
            (r"/accounts/login", AccountsLoginHandler),

            # ...

        ]

* ``static/``

    Static files (JavaScript, CSS, images, user media, etc.) go here. You can change the default path
    by specifying ``settings.static_path``

* ``templates/``

    Templates here. Change via ``settings.template_path``

* ``flashpolicy.xml``

    Defines Flash policy for older browsers (not supporting WebSockets). It is possible that you
    will never need to change this file. It is, however, required by Airy.

* ``manage.py``

    A basic python script that invokes **Airy**. You wouldn't normally need to change it.
    It comes with every new project created via ``airy-admin.py``

* ``settings.py``

    Your project's settings file. Technically it's just a python file, so you can use it
    to override default settings (like ``settings.static_path`` or ``settings.port``) or
    just specify it at run time as an argument.

    See :doc:`Command-line Interface <05_console>` for details.
