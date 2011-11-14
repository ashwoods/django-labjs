from __future__ import with_statement
import os
import codecs

from django.template import Context
from django.template.loader import render_to_string
from django.utils.encoding import smart_unicode
from compressor.utils import get_class
from compressor.utils.decorators import cached_property, memoize

class Labjs(object):
    """
    """

    def __init__(self, content=None, context=None, *args, **kwargs):
        self.content = content
        self.context = context
        self.split_content = []

    @cached_property
    def parser(self):
        return get_class(settings.COMPRESS_PARSER)(self.content)

    def split_contents(self):
        if self.split_content:
            return self.split_content
        for elem in self.parser.js_elems():
            attribs = self.parser.elem_attribs(elem)
            if 'src' in attribs:
                basename = self.get_basename(attribs['src'])
                self.split_content.append(basename)
            else: # TODO: what do we when its not, raise error?
                content = self.parser.elem_content(elem)

        return self.split_content

    def render_output(self, context=None):
        """
        """
        if context is None:
            context = {}
        return render_to_string("labjs/labjs.html", final_context)
