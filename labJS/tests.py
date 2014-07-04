# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.test.client import RequestFactory
from django.test.utils import override_settings

from labJS.base import Labjs
from labJS.templatetags.labjs import LabjsNode


class FakeNode(object):

    def render(self, context):
        return 'some content'


class TestLabjs(TestCase):

    def test_split_contents_empty_content(self):
        lab = Labjs('')
        self.assertFalse(lab.split_contents())

    def test_split_contents_non_js_content(self):
        lab = Labjs('<p class="test">I am not JS</p>')
        self.assertFalse(lab.split_contents())

    def test_split_contents_inline(self):
        lab = Labjs('<script>document.write("Hello world");</script>')
        self.assertEqual(
            lab.split_contents(),
            [{'data': 'document.write("Hello world");', 'type': 'inline'}]
        )

    def test_split_contents_script(self):
        lab = Labjs('<script src="/static/script.js"></script>')
        self.assertEqual(
            lab.split_contents(),
            [{'data': '/static/script.js', 'type': 'script'}]
        )


class TestLabjsNode(TestCase):

    @override_settings(LABJS_DEBUG_TOGGLE='labjs')
    def test_debug_mode_no_request_context(self):
        node = LabjsNode(None)
        context = {}
        self.assertFalse(node.debug_mode(context))

    @override_settings(LABJS_DEBUG_TOGGLE='labjs')
    def test_debug_mode_no_toggle(self):
        node = LabjsNode(None)
        context = {
            'request': RequestFactory().get('/'),
        }
        self.assertFalse(node.debug_mode(context))

    @override_settings(LABJS_DEBUG_TOGGLE='labjs')
    def test_debug_mode_with_toggle(self):
        node = LabjsNode(None)
        context = {
            'request': RequestFactory().get('/?labjs=1'),
        }
        self.assertTrue(node.debug_mode(context))

    @override_settings(LABJS_DEBUG_TOGGLE=None)
    def test_debug_mode_setting_undefined(self):
        node = LabjsNode(None)
        context = {
            'request': RequestFactory().get('/?labjs='),
        }
        self.assertFalse(node.debug_mode(context))

    @override_settings(LABJS_ENABLED=False)
    def test_disabled_leaves_content_as_original(self):
        node = LabjsNode(FakeNode())
        context = {
            'request': RequestFactory().get('/?labjs='),
        }
        self.assertEqual(node.render(context), 'some content')
