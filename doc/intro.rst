Introduction
============

Airy is a new Web application development framework. Contrast to most currently available frameworks,
Airy doesn't use the standard notion of HTTP requests and pages. Instead, it makes use of WebSockets
and provides a set of tools to let you focus on the interface, not content delivery.

Currently Airy supports MongoDB only. We plan to provide support for other NoSQL databases,
but we have no plans for supporting SQL.

Airy includes or otherwise uses a set of tools and third-party libraries. For a full list of
modules see `Acknowledgement`_

WebSockets
----------

Airy uses WebSockets for all client-server communication.

On older browsers it degrades to AJAX polling or Flash (or HTML File), thanks to
`Socket.io <http://socket.io>`_ and `TornadIO2 <https://github.com/MrJoes/tornadio2>`_
that are used throughout Airy.

This means that Airy comes with real-time support built-in which works on any modern browser.

Database
--------

Only MongoDB is currently supported. We welcome any help in porting Airy to other database engines, but we
have no plans for supporting SQL.

Airy comes with a basic ORM, which is provided by `MongoEngine <http://mongoengine.org/>`_

Please refer to the `MongoEngine Documentation <http://mongoengine.org/docs/>`_ for details on how to use the database layer.

Interface
---------

By default, Airy includes `Foundation CSS Framework <http://foundation.zurb.com/>`_ (by `ZURB <http://www.zurb.com/>`_) in every new project. This will become
optional in future releases and we will also add support for `Twitter Bootstrap <http://twitter.github.com/bootstrap/>`_

Airy also includes a small JavaScript library that is responsible for establishing initial Socket.io connection.
Additionally, it modifies web page content and sends all requests via the connection instead of initiating a plain HTTP request.

Acknowledgement
---------------

Airy is built on top of and relies on the following tools and libraries:

* `Tornado <http://www.tornadoweb.org/>`_
* `MongoEngine <http://mongoengine.org/>`_
* `Socket.io <http://socket.io>`_
* `TornadIO2 <https://github.com/MrJoes/tornadio2>`_
* `jQuery <http://jquery.com/>`_
* `jQuery History Plugin <https://github.com/balupton/jquery-history>`_
* `jQuery Cookie Plugin <https://github.com/carhartl/jquery-cookie>`_

Additionally, a part of `Django <http://djangoproject.com/>`_ has been ported to Airy, specifically Django Forms,
File handling library, markup utils and more.

