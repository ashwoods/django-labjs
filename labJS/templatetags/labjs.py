from django import template
from django.core.exceptions import ImproperlyConfigured

#rom compressor.cache import (cache_get, cache_set, get_offline_hexdigest,
#                             get_offline_manifest, get_templatetag_cachekey)
from labJS.conf import settings
from labJS.base import Labjs
from django.utils.safestring import mark_safe

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

    def render(self, context):
        #Check if in debug mode
        if self.debug_mode(context) or settings.LABJS_ENABLED:
            return self.nodelist.render(context)


        # call compressor output method and handle exceptions
        rendered_output = Labjs(content=self.nodelist.render(context),context=context).render_output()
        #if cache_key:
        #    cache_set(cache_key, rendered_output)
        return rendered_output


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

        <script type="text/javascript" src="{{ STATIC_URL }}js/jquery-1.5.2.min.js" ></script>

        {% wait %}

        <script type="text/javascript" src="{{ STATIC_URL }}js/jquery.formset.min.js" ></script>
        <script type="text/javascript" src="{% url django.views.i18n.javascript_catalog %}"></script>

    {% endlabjs %}


    Which would be rendered something like::

     <script type="text/javascript">$LAB.queueScript("/static/js/jquery-1.5.2.min.js").queueScript("/static/js/jquery.formset.min.js").queueScript("/jsi18n/")</script>

    """
    chunks = []
    while True:
        nodelist = parser.parse(('wait',')
        chunks.append(nodelist)

    ptoken = parser.next_token()
    if ptoken.contents == 'wait':
        print ptokn
    else:
        parser.delete_first_token()
    return LabjsNode(nodelist)


#@register.simple_tag(takes_context=True)
#def wait(context):
#    """
#    Renders an empty labjs queue
#    """
#    return '<script type="text/javascript"></script>' #TODO: make this prettier





