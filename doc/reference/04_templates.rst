Templates
====================================

Overview
--------

Airy relies on `Tornado <http://www.tornadoweb.org/>`_ for templating.

Currently, Airy provides server-side templates only. We plan to introduce
client-side templates in the future.

Template Reference
------------------

This is an excerpt from `Tornado documentation <http://www.tornadoweb.org/documentation/template.html>`_.

We compile all templates to raw Python. Error-reporting is currently... uh,
interesting. Syntax for the templates::

    ### base.html
    <html>
      <head>
        <title>{% block title %}Default title{% end %}</title>
      </head>
      <body>
        <ul>
          {% for student in students %}
            {% block student %}
              <li>{{ escape(student.name) }}</li>
            {% end %}
          {% end %}
        </ul>
      </body>
    </html>

    ### bold.html
    {% extends "base.html" %}

    {% block title %}A bolder title{% end %}

    {% block student %}
      <li><span style="bold">{{ escape(student.name) }}</span></li>
    {% end %}

Unlike most other template systems, we do not put any restrictions on the
expressions you can include in your statements. if and for blocks get
translated exactly into Python, you can do complex expressions like::

   {% for student in [p for p in people if p.student and p.age > 23] %}
     <li>{{ escape(student.name) }}</li>
   {% end %}

Translating directly to Python means you can apply functions to expressions
easily, like the escape() function in the examples above. You can pass
functions in to your template just like any other variable::

   ### Python code
   def add(x, y):
      return x + y
   template.execute(add=add)

   ### The template
   {{ add(1, 2) }}

We provide the functions escape(), url_escape(), json_encode(), and squeeze()
to all templates by default.

Typical applications do not create `Template` or `Loader` instances by
hand, but instead use the `render` and `render_string` methods of
`tornado.web.RequestHandler`, which load templates automatically based
on the ``template_path`` `Application` setting.

Syntax Reference
----------------

Template expressions are surrounded by double curly braces: ``{{ ... }}``.
The contents may be any python expression, which will be escaped according
to the current autoescape setting and inserted into the output.  Other
template directives use ``{% %}``.  These tags may be escaped as ``{{!``
and ``{%!`` if you need to include a literal ``{{`` or ``{%`` in the output.

To comment out a section so that it is omitted from the output, surround it
with ``{# ... #}``.

``{% apply *function* %}...{% end %}``
    Applies a function to the output of all template code between ``apply``
    and ``end``::

        {% apply linkify %}{{name}} said: {{message}}{% end %}

``{% autoescape *function* %}``
    Sets the autoescape mode for the current file.  This does not affect
    other files, even those referenced by ``{% include %}``.  Note that
    autoescaping can also be configured globally, at the `Application`
    or `Loader`.::

        {% autoescape xhtml_escape %}
        {% autoescape None %}

``{% block *name* %}...{% end %}``
    Indicates a named, replaceable block for use with ``{% extends %}``.
    Blocks in the parent template will be replaced with the contents of
    the same-named block in a child template.::

        <!-- base.html -->
        <title>{% block title %}Default title{% end %}</title>

        <!-- mypage.html -->
        {% extends "base.html" %}
        {% block title %}My page title{% end %}

``{% comment ... %}``
    A comment which will be removed from the template output.  Note that
    there is no ``{% end %}`` tag; the comment goes from the word ``comment``
    to the closing ``%}`` tag.

``{% extends *filename* %}``
    Inherit from another template.  Templates that use ``extends`` should
    contain one or more ``block`` tags to replace content from the parent
    template.  Anything in the child template not contained in a ``block``
    tag will be ignored.  For an example, see the ``{% block %}`` tag.

``{% for *var* in *expr* %}...{% end %}``
    Same as the python ``for`` statement.

``{% from *x* import *y* %}``
    Same as the python ``import`` statement.

``{% if *condition* %}...{% elif *condition* %}...{% else %}...{% end %}``
    Conditional statement - outputs the first section whose condition is
    true.  (The ``elif`` and ``else`` sections are optional)

``{% import *module* %}``
    Same as the python ``import`` statement.

``{% include *filename* %}``
    Includes another template file.  The included file can see all the local
    variables as if it were copied directly to the point of the ``include``
    directive (the ``{% autoescape %}`` directive is an exception).
    Alternately, ``{% module Template(filename, **kwargs) %}`` may be used
    to include another template with an isolated namespace.

``{% module *expr* %}``
    Renders a `~tornado.web.UIModule`.  The output of the ``UIModule`` is
    not escaped::

        {% module Template("foo.html", arg=42) %}

``{% raw *expr* %}``
    Outputs the result of the given expression without autoescaping.

``{% set *x* = *y* %}``
    Sets a local variable.

``{% try %}...{% except %}...{% finally %}...{% end %}``
    Same as the python ``try`` statement.

``{% while *condition* %}... {% end %}``
    Same as the python ``while`` statement.


Context Processors
------------------

You may want to extend the default functionality with your own tags.
Airy provides that functionality by means of context processors.

A context processor is a simple function that takes the current ``handler`` and
optionally any other arguments and returns a dictionary. Keys are used
as names for injecting into template namespace.

For example, to add a variable containing the current user into global namespace:

.. code-block:: python

    # snippet from users/context_processors.py

    def user(handler, **kwargs):
        return {'user': handler.get_current_user()}

Then add your context processor to settings:

.. code-block:: python

    # settings.py

    template_context_processors = [
        # ...
        'users.context_processors.user',
    ]

Now you can access ``user`` throughout your templates, for example:

.. code-block:: html

    <p>
        Hello, {{ user.username }}
    </p>

Note that by default Airy inserts ``users.context_processors.user`` in every new project.


Markup Processor
----------------

Airy also comes with a markup module to make templating easier.

By default, every new project has ``airy.core.context_processors.markup``, which allows you
to use the following methods: linebreaks(), linkify(), sanitize() and truncate()

Example Usage
^^^^^^^^^^^^^

.. code-block:: html

    <ul>
    {% for message in messages %}
        <li>
            <p>
                From: {{ message.sender }}
            </p>
            <p>
                {% apply markup.linebreaks %}
                    {{ message.body }}
                {% end %}
            </p>
        </li>
    {% end %}
    </ul>


Method Reference
^^^^^^^^^^^^^^^^

.. automodule:: airy.core.markup
   :members:
   :show-inheritance:

