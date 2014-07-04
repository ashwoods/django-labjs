# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from compressor.conf import settings
from compressor.utils import get_class
from compressor.utils.decorators import cached_property
from django.template import Context
from django.template.loader import render_to_string
from django.utils.encoding import smart_text
from django.utils.safestring import mark_safe


class Labjs(object):
    """
    Parses html for javascript elements and returns the LabJS html.
    """

    def __init__(self, content=None, context=None, type=None, *args, **kwargs):
        self.content = content
        self.context = context or {}
        self.queue = []

    @cached_property
    def parser(self):
        return get_class(settings.COMPRESS_PARSER)(self.content)

    def split_contents(self):
        """
        Parses html for javascript
        """
        if self.queue:
            return self.queue
        for elem in self.parser.js_elems():
            attribs = self.parser.elem_attribs(elem)
            if 'src' in attribs:
                basename = attribs['src']
                self.queue.append({
                    'data': basename,
                    'type': 'script',
                })
            else:
                # TODO: fix this evil fix when compressor bug fixed
                content = self.parser.elem_content(elem)
                if content == "None":
                    content = ""
                self.queue.append({
                    'data': content,
                    'type': 'inline',
                })
        return self.queue

    def render_output(self, context=None):
        """
        Renders the LabJS output
        """
        if context is None:
            context = {}
        final_context = Context()
        final_context.update(self.context)
        final_context.update(context)

        inner_content = smart_text('')
        queue = self.split_contents()

        for js in queue:
            if js['type'] == 'script':
                rendered = mark_safe(render_to_string(
                    'labjs/labjs.html', {'js': js['data']}
                ))
                inner_content += rendered
            else:
                rendered = render_to_string(
                    'labjs/wait.html',  {'js': mark_safe(js['data'])}
                )
                inner_content += rendered

        final_context.update({'js': mark_safe(inner_content)})
        return render_to_string('labjs/header.html', final_context)
