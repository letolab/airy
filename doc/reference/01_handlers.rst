Handlers
====================================

Overview
--------

In every project, you would normally have a single handler subclassing
:py:class:`~airy.core.web.AiryRequestHandler` to process ordinary HTTP requests.

This handler should be responsible for rendering basic HTML page and establishing
Socket.io connection.

If you've used ``airy-admin.py startproject`` to create your project, you should already
have such handler in ``users/handlers.py`` and a bunch of other Socket.io handlers (subclassing
:py:class:`~airy.core.web.AiryHandler`)

When a Socket.io connection is established, Airy sends all data over that connection and
emulates the standard GET/POST behaviour for ordinary links and all forms in your project.

You safely push HTML data to the client and Airy will adjust forms and links to use Socket.io
connection instead of making an HTTP request every time.

If you creating your project manually from scratch, you may want add a 'core' app (such as users)
with the following code to implement the functionality:

.. code-block:: python

    from airy.core.web import AiryHandler, AiryRequestHandler

    class IndexHandler(AiryRequestHandler):
        """
        This is a standard old-style HTTP handler.

        When a client makes initial HTTP request it will render the basic page
        containing all the required elements.
        """
        def get(self):
            self.render("base.html")

            """
            The file 'base.html' may look like this:

            <html>
            <head>
                <title>My Airy Project</title>

                <!-- Airy JavaScript files - required -->
                <script type="text/javascript" src="/airy/lib/jquery-1.6.1.min.js"></script>
                <script type="text/javascript" src="/airy/lib/jquery.history.js"></script>
                <script type="text/javascript" src="/airy/lib/jquery.serializeForm.js"></script>
                <script type="text/javascript" src="/airy/lib/jquery.cookie.js"></script>
                <script type="text/javascript" src="/airy/socket.io.js"></script>
                <script type="text/javascript" src="/airy/airy.js"></script>

            </head>
            <body>
                <div id="content">
                </div>
            </body>
            </html>

            """


    class HomeHandler(AiryHandler):
        """
        This is an example of a Socket.io handler where all data is
        """
        def get(self):
            self.render("#content", "index.html", user=self.get_current_user())

            """
            The file 'index.html' may look like this:

            <p>Hello, {{ user.username }}!</p>

            """

Note:

    The JavaScript files (included in the base.html example above) are responsible for managing
    Socket.io communication. If you don't include them, your project will work just like an ordinary
    Tornado website. No handlers subclassing AiryHandler will be invoked - Airy will just ignore them.


Class Reference
---------------

.. autoclass:: airy.core.web.AiryRequestHandler
   :members:
   :inherited-members:
   :member-order: bysource

.. autoclass:: airy.core.web.AiryHandler
   :members:
   :inherited-members:
   :member-order: bysource

    .. attribute:: site

        An :py:class:`~airy.core.web.AirySite` object containing all current connections. Each
        AiryHandler refers to the same AirySite, which allows you to send data between site users.
        See :py:attr:`~AirySite.connections` for more details.

    .. attribute:: arguments

        A dictionary containing all arguments sent with the request (e.g. a form data for a POST-like request).

    .. attribute:: files

        A dictionary with all the files sent with the request. Each file is an
        ``airy.core.files.uploadedfile.SimpleUploadedFile`` instance.

    .. attribute:: connection

        Current connection object with all related metadata.

.. autoclass:: airy.core.web.AirySite
   :members:
   :inherited-members:
   :member-order: bysource

    .. attribute:: connections

        A ``set`` with all current connections. Each connection has a ``state`` attribute, which
        contains the most recently requested URL. You can iterate over the connections to send data
        between users, for example:

        .. code-block:: python

            class MessagesHandler(AiryHandler):

                # ...

                def post(self, path):
                    "Send a message to all current visitors"

                    form = MessageForm(self.get_flat_arguments())
                    if form.is_valid():
                        message = form.save(self)

                        for conn in self.site.connections:
                            if conn.state == '/chat/' or conn == self.connection:
                                conn.append(
                                    '#message-thread',
                                    self.render_string('messaging/message.html', message=reply)
                                )





