Command-line Interface
====================================

airy-admin.py
-------------

Airy comes with a handy admin script: ``airy-admin.py``

You would normally use it to create a new project or a new app within an existing project.

**Available commands:**

* ``startproject <project_name>:``

    Creates a new project in a folder named <project_name>

* ``startapp <app_name>:``

    Creates a new app in a folder named <app_name>

* ``help:``

    Displays this help


manage.py
---------

When you create a new project using ``airy-admin.py`` Airy automatically adds a ``manage.py`` script.

**Available commands:**

* ``run [OPTIONS]``

    Starts Tornado web server. For a full list of options type ``python manage.py help``

* ``runserver [OPTIONS]``

    An alias of ``run``.

* ``shell [OPTIONS]``

    Sets up the environment (connects to the DB, imports modules) and starts IPython shell.

* ``help``

    Print a list of available options.
