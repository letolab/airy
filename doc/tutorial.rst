Quick Tutorial
====================================

Installation
------------

To install **Airy**, run:

.. code-block:: console

    # pip install airy

Airy needs a running `MongoDB <http://www.mongodb.org/>`_ server. Please refer to the relevant page in MongoDB docs
regarding MongoDB installation.

Creating new project
--------------------

Once you have installed Airy, you should have the ``airy-admin.py`` script available.

Open a Terminal, navigate to some directory where you want to create a new project and type:

.. code-block:: console

    $ airy-admin.py startproject project_name
    $ cd project_name


Configuration
-------------

Edit the ``settings.py`` file in the project directory.

Make sure you change the ``database_name`` and the ``cookie_secret``:

.. code-block:: python

    ...

    database_name = 'airydb' # replace with your DB name

    ...

    cookie_secret = 'airy_secret' # replace with yours

    ...


Starting up
-----------

Run ``update_ve`` to download and build all the required modules, then start your project:

    $ python manage.py update_ve
    $ python manage.py run

You should see something like this:

.. code-block:: none

    [I 120131 11:30:01 server:86] Starting up tornadio server on port '8000'
    [I 120131 11:30:01 server:93] Starting Flash policy server on port '8043'
    [I 120131 11:30:01 server:103] Entering IOLoop...

Then open your browser and navigate to http://localhost:8000/

Hopefully you will see the default Airy welcome page.


