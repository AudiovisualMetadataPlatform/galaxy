# -*- coding:ascii -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1568307820.455017
_enable_loop = True
_template_filename = 'templates/base.mako'
_template_uri = '/base.mako'
_source_encoding = 'ascii'
_exports = ['title', 'stylesheets', 'init', 'javascript_app', 'javascripts', 'metas']


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    ns = runtime.TemplateNamespace(u'galaxy_client', context._clean_inheritance_tokens(), templateuri=u'/galaxy_client_app.mako', callables=None,  calling_uri=_template_uri)
    context.namespaces[(__name__, u'galaxy_client')] = ns

def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        h = context.get('h', UNDEFINED)
        self = context.get('self', UNDEFINED)
        next = context.get('next', UNDEFINED)
        app = context.get('app', UNDEFINED)
        n_ = context.get('n_', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n')
        self.js_app = None 
        
        __M_locals_builtin_stored = __M_locals_builtin()
        __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in [] if __M_key in __M_locals_builtin_stored]))
        __M_writer(u'\n\n')
        _=n_ 
        
        __M_locals_builtin_stored = __M_locals_builtin()
        __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['_'] if __M_key in __M_locals_builtin_stored]))
        __M_writer(u'\n<!DOCTYPE HTML>\n<html>\n    <!--base.mako-->\n    ')
        __M_writer(unicode(self.init()))
        __M_writer(u'\n    <head>\n        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\n')
        __M_writer(u'        <meta name = "viewport" content = "maximum-scale=1.0">\n')
        __M_writer(u'        <meta http-equiv="X-UA-Compatible" content="IE=Edge,chrome=1">\n\n        <title>\n            Galaxy\n')
        if app.config.brand:
            __M_writer(u'            | ')
            __M_writer(unicode(app.config.brand))
            __M_writer(u'\n')
        __M_writer(u'            | ')
        __M_writer(unicode(self.title()))
        __M_writer(u'\n        </title>\n')
        __M_writer(u'        <link rel="index" href="')
        __M_writer(unicode( h.url_for( '/' ) ))
        __M_writer(u'"/>\n        ')
        __M_writer(unicode(self.metas()))
        __M_writer(u'\n        ')
        __M_writer(unicode(self.stylesheets()))
        __M_writer(u'\n        ')
        __M_writer(unicode(self.javascripts()))
        __M_writer(u'\n        ')
        __M_writer(unicode(self.javascript_app()))
        __M_writer(u'\n    </head>\n    <body class="inbound">\n        ')
        __M_writer(unicode(next.body()))
        __M_writer(u'\n    </body>\n</html>\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_title(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_stylesheets(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n    ')
        __M_writer(unicode(h.css("base")))
        __M_writer(u'\n    ')
        __M_writer(unicode(h.css('bootstrap-tour')))
        __M_writer(u'\n    ')
        __M_writer(unicode(h.css('base')))
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_init(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_javascript_app(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        self = context.get('self', UNDEFINED)
        galaxy_client = _mako_get_namespace(context, 'galaxy_client')
        __M_writer = context.writer()
        __M_writer(u'\n    ')
        __M_writer(unicode( galaxy_client.load( app=self.js_app ) ))
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_javascripts(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)
        app = context.get('app', UNDEFINED)
        trans = context.get('trans', UNDEFINED)
        form_input_auto_focus = context.get('form_input_auto_focus', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n')
        if app.config.sentry_dsn:
            __M_writer(u'        ')
            __M_writer(unicode(h.js( "libs/raven" )))
            __M_writer(u"\n        <script>\n            Raven.config('")
            __M_writer(unicode(app.config.sentry_dsn_public))
            __M_writer(u"').install();\n")
            if trans.user:
                __M_writer(u'                Raven.setUser( { email: "')
                __M_writer(filters.html_escape(unicode(trans.user.email)))
                __M_writer(u'" } );\n')
            __M_writer(u'        </script>\n')
        __M_writer(u'\n    ')
        __M_writer(unicode(h.js(
        ## TODO: remove when all libs are required directly in modules
        'libs/require',
        'bundled/libs.chunk',
        'bundled/base.chunk',
        'bundled/extended.bundled'
    )))
        __M_writer(u'\n\n')
        if not form_input_auto_focus is UNDEFINED and form_input_auto_focus:
            __M_writer(u'        <script type="text/javascript">\n            $(document).ready( function() {\n                // Auto Focus on first item on form\n                if ( $("*:focus").html() == null ) {\n                    $(":input:not([type=hidden]):visible:enabled:first").focus();\n                }\n            });\n        </script>\n')
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_metas(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "ascii", "line_map": {"131": 49, "139": 49, "140": 51, "141": 52, "142": 52, "143": 52, "144": 54, "145": 54, "146": 55, "147": 56, "148": 56, "149": 56, "150": 58, "23": 1, "152": 61, "26": 0, "159": 67, "160": 69, "161": 70, "162": 79, "36": 1, "37": 2, "177": 168, "168": 87, "41": 2, "42": 4, "151": 60, "46": 4, "47": 8, "48": 8, "49": 12, "50": 14, "51": 18, "52": 19, "53": 19, "54": 19, "55": 21, "56": 21, "57": 21, "58": 24, "59": 24, "60": 24, "61": 25, "62": 25, "63": 26, "64": 26, "65": 27, "66": 27, "67": 28, "68": 28, "69": 31, "70": 31, "71": 36, "72": 39, "73": 46, "74": 80, "75": 84, "76": 87, "82": 36, "91": 42, "96": 42, "97": 43, "98": 43, "99": 44, "100": 44, "101": 45, "102": 45, "108": 39, "117": 82, "123": 82, "124": 83, "125": 83}, "uri": "/base.mako", "filename": "templates/base.mako"}
__M_END_METADATA
"""
