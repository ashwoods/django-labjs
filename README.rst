Django LabJS
============

Labjs is a django-compressor_ *plugin* that provides django templatetags to easily Labify your scripts, using
the `labjs javascript loader`_.


Together with django-compressor it can make downloading your js files extremely efficient.


What is LabJS?
--------------

LABjs (Loading And Blocking JavaScript) is an open-source (MIT license) project supported by Getify Solutions.
The core purpose of LABjs is to be an all-purpose, on-demand JavaScript loader, capable of loading any JavaScript resource,
from any location, into any page, at any time. Loading your scripts with LABjs reduces resource blocking during page-load,
which is an easy and effective way to optimize your site's performance.


LABjs by default will load (and execute) all scripts in parallel as fast as the browser will allow.
However, you can easily specify which scripts have execution order dependencies and LABjs will ensure proper execution order.
This makes LABjs safe to use for virtually any JavaScript resource, whether you control/host it or not,
and whether it is standalone or part of a larger dependency tree of resources.


Using LABjs will replace all that ugly "<script> tag soup" -- that is all the <script> tags that commonly appear
in the ``<head>`` or end of the ``<body>`` of your HTML page. The API is expressive and chaining, to let you specify which
scripts to load, and when to wait ("block"), if necessary, for execution before proceeding with further execution.
The API also easily allows inline code execution coupling (think: inline ``<script>`` tags).


Django-labjs uses labjs queues
______________________________


In order to make it easy to use labjs with the django templating system, django-labjs implements labjs using it's
queuing features::


    $LAB
	    .queueScript("script1.js") // script1, script2, and script3 do not depend on each other
	    .queueScript("script2.js") // so execute in any order
	    .queueScript("script3.js")

	    .queueWait(function(){  // can still have executable wait(...) functions if you need to
	        alert("Scripts 1-3 are loaded!");
	    })
	    .queueScript("script4.js") // depends on script1, script2 and script3 being executed before
	    .queueWait(function(){script4Func();});


And somewhere close to the closing ``</body>`` tag::


	$LAB
	    .runQueue() // execute the queue as a $LAB chain


Installation
------------

Currently available only on github, install using pip::

    pip install -e git+git://github.com/ashwoods/django-labjs.git


Usage
-----

Include the labjs javascript file somewhere in your html templates under ``<head>``. Don't forget to include labjs
templatetags, and wrap javascript imports AND any javascript inlines that depend on those imports between
``{% labjs %}`` and ``{% endlabjs %}`` tags. Use ``{% wait %}`` tags to insert an empty ``queuewait()``

Usage example::

    <script type="text/javascript" src="{{ STATIC_URL}}labjs/LAB.min.js"></script>

    {% labjs %}
    <script type="text/javascript" src="src/path_to_js.js" />
    ...
    ...

    {% wait %} // use wait to insert an empty .queueWait()

    // You have to place any inline javascript that depends on any of the Labified scripts
    // under a labjs templatetag. It will automatically place it under a queueWait.

    <script type="text/javascript">
    ...
    ...
    <script>

    {% endlabjs %}

    ...
    ...

    // At almost end of page run the queue, either with the {% runqueue %} templatetag
    // or manually if you want to add custom waits and queue some more scripts.


    {% runlabjs %}


Settings
--------

For now, django Labjs uses django-compressor parsers, so any settings on which parser to use
with django-compressor affects which html parsers django-labjs uses.

The only labjs specific setting is ``LABJS_ENABLED``, that defaults to the opposite of ``DEBUG``.
When ``LABJS_ENABLED`` is False, the templatetags do nothing.

Tips
----


When using labjs, labjs ensures that the javascript you need has already ran through the use
of waits. This functionality is normally achieved by using shortcut functions like jquery's ``$.ready()``.
When using labjs, however, ready() is not only needed, but might be slightly counterproductive.
``$.ready()`` waits for browser dom ready, which you need if you are going to be doing dom interaction.
Otherwise, it might not be necessary. For more information, read this stack `answer`_.

.. _answer: http://stackoverflow.com/a/5409818/471842
.. _labjs javascript loader: http://labjs.com
.. _django-compressor: http://github.com/jezdez/django_compressor
