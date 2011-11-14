from django import template
from django.core.exceptions import ImproperlyConfigured

#rom compressor.cache import (cache_get, cache_set, get_offline_hexdigest,
#                             get_offline_manifest, get_templatetag_cachekey)
from labjs.conf import settings
from labjs.base import Labjs

register = template.Library()

class LabNode(template.Node):

    def __init__(self, nodelist):
        self.nodelist = nodelist

    def compressor_cls(self, *args, **kwargs):
        
        return get_class(compressors.get(self.kind),
                         exception=ImproperlyConfigured)(*args, **kwargs)

    def debug_mode(self, context):
        if settings.LABJS_DEBUG_TOGGLE:
            # Only check for the debug parameter
            # if a RequestContext was used
            request = context.get('request', None)
            if request is not None:
                return settings.LABJS_DEBUG_TOGGLE in request.GET

    def render(self, context, forced=False):
        # Check if in debug mode
        if self.debug_mode(context):
            return self.nodelist.render(context)

        # Prepare the compressor
        compressor = self.compressor_cls(content=self.nodelist.render(context),
                                         context=context)

        # Check cache
        #cache_key, cache_content = self.render_cached(compressor, forced)
        #if cache_content is not None:
        #    return cache_content

        # call compressor output method and handle exceptions
        rendered_output = compressor.output(self.mode, forced=forced)
        #if cache_key:
        #    cache_set(cache_key, rendered_output)
        return rendered_output


@register.tag
def lab(parser, token):
    """
    Renders a labjs queue from linked or inline js.

    Syntax::

        {% labjs %}
        <html of inline or linked JS/CSS>
        {% endlabjs %}

    Examples::

        {%  labjs %}
        <script src="/media/js/one.js" type="text/javascript" charset="utf-8"></script>
        {% endlabjs %}

    Which would be rendered something like::

        <script type="text/javascript" src="/media/CACHE/js/3f33b9146e12.js" charset="utf-8"></script>

    """

    nodelist = parser.parse(('endlabjs',))
    parser.delete_first_token()



    return LabjsNode(nodelist)
