# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import template
from django.template import NodeList

from labJS.base import Labjs
from labJS.conf import settings


register = template.Library()


class LabjsNode(template.Node):

    def __init__(self, nodelist, *args, **kwargs):
        self.nodelist = nodelist

    def debug_mode(self, context):
        if settings.LABJS_DEBUG_TOGGLE:
            # Only check for the debug parameter
            # if a RequestContext was used
            request = context.get('request', None)
            if request is not None:
                return settings.LABJS_DEBUG_TOGGLE in request.GET
        return False

    def render(self, context):
        # Check if in debug mode
        if self.debug_mode(context) or not settings.LABJS_ENABLED:
            return self.nodelist.render(context)

        # call compressor output method and handle exceptions
        rendered_output = Labjs(
            content=self.nodelist.render(context),
            context=context
        ).render_output()
        return rendered_output


class Wait(template.Node):

    def render(self, context):
        # TODO: implement check
        return '<script type="text/javascript"></script>'


@register.tag
def labjs(parser, token):
    """
    Renders a labjs queue from linked js.

    Syntax::

        {% labjs %}
        <html of linked JS>
        {% endlabjs %}

    Examples::

    {% labjs %}

        <script
            type="text/javascript"
            src="{{ STATIC_URL }}js/jquery-1.5.2.min.js">
        </script>

        {% wait %}

        <script
            type="text/javascript"
            src="{{ STATIC_URL }}js/jquery.formset.min.js">
        </script>
        <script
            type="text/javascript"
            src="{% url django.views.i18n.javascript_catalog %}">
        </script>

    {% endlabjs %}

    Which would be rendered something like::

     <script type="text/javascript">
        $LAB.queueScript("/static/js/jquery-1.5.2.min.js")
            .queueScript("/static/js/jquery.formset.min.js")
            .queueScript("/jsi18n/");
    </script>

    """
    nodelist = NodeList()
    while True:
        chunk = parser.parse(('endlabjs', 'wait'))
        ptoken = parser.next_token()

        if ptoken.contents == 'wait':
            chunk.append(Wait())
            nodelist.extend(chunk)
        elif ptoken.contents == 'endlabjs':
            nodelist.extend(chunk)
            break

    return LabjsNode(nodelist)


@register.simple_tag
def runlabjs():
    """
    Renders an empty labjs queue
    """
    # TODO: make this prettier
    return '<script type="text/javascript">$LAB.runQueue();</script>'
