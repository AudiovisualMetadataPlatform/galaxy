# -*- coding:ascii -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1568307820.439111
_enable_loop = True
_template_filename = u'templates/message.mako'
_template_uri = u'/message.mako'
_source_encoding = 'ascii'
_exports = ['body', 'render_msg', 'init', 'javascripts', 'center_panel']



import bleach

def inherit(context):
    if context.get('use_panels'):
        if context.get('webapp'):
            app_name = context.get('webapp')
        elif context.get('app'):
            app_name = context.get('app').name
        else:
            app_name = 'galaxy'
        return '/webapps/%s/base_panels.mako' % app_name
    else:
        return '/base.mako'


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    ns = runtime.TemplateNamespace('__anon_0x13773c590', context._clean_inheritance_tokens(), templateuri=u'/refresh_frames.mako', callables=None,  calling_uri=_template_uri)
    context.namespaces[(__name__, '__anon_0x13773c590')] = ns

def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, (inherit(context)), _template_uri)
def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x13773c590')._populate(_import_ns, [u'handle_refresh_frames'])
        n_ = _import_ns.get('n_', context.get('n_', UNDEFINED))
        __M_writer = context.writer()
        __M_writer(u'\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        _=n_ 
        
        __M_locals_builtin_stored = __M_locals_builtin()
        __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['_'] if __M_key in __M_locals_builtin_stored]))
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_body(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x13773c590')._populate(_import_ns, [u'handle_refresh_frames'])
        status = _import_ns.get('status', context.get('status', UNDEFINED))
        message = _import_ns.get('message', context.get('message', UNDEFINED))
        def render_msg(msg,status='done'):
            return render_render_msg(context,msg,status)
        __M_writer = context.writer()
        __M_writer(u'\n    ')
        __M_writer(unicode(render_msg( message, status )))
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_render_msg(context,msg,status='done'):
    __M_caller = context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x13773c590')._populate(_import_ns, [u'handle_refresh_frames'])
        _ = _import_ns.get('_', context.get('_', UNDEFINED))
        __M_writer = context.writer()
        __M_writer(u'\n    ')

        if status == "done":
            status = "success"
        elif status == "error":
            status = "danger"
        if status not in ("danger", "info", "success", "warning"):
            status = "info"
            
        
        __M_writer(u'\n    <div class="mt-2 alert alert-')
        __M_writer(unicode(status))
        __M_writer(u'">')
        __M_writer(unicode(_(bleach.clean(msg))))
        __M_writer(u'</div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_init(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x13773c590')._populate(_import_ns, [u'handle_refresh_frames'])
        self = _import_ns.get('self', context.get('self', UNDEFINED))
        active_view = _import_ns.get('active_view', context.get('active_view', UNDEFINED))
        __M_writer = context.writer()
        __M_writer(u'\n')

        self.has_left_panel=False
        self.has_right_panel=False
        self.active_view=active_view
        self.message_box_visible=False
        
        
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_javascripts(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x13773c590')._populate(_import_ns, [u'handle_refresh_frames'])
        handle_refresh_frames = _import_ns.get('handle_refresh_frames', context.get('handle_refresh_frames', UNDEFINED))
        parent = _import_ns.get('parent', context.get('parent', UNDEFINED))
        __M_writer = context.writer()
        __M_writer(u'\n    ')
        __M_writer(unicode(parent.javascripts()))
        __M_writer(u'\n    ')
        __M_writer(unicode(handle_refresh_frames()))
        __M_writer(u'\n    <script type="text/javascript">\n        if ( parent.handle_minwidth_hint )\n        {\n            parent.handle_minwidth_hint( -1 );\n        }\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_center_panel(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x13773c590')._populate(_import_ns, [u'handle_refresh_frames'])
        status = _import_ns.get('status', context.get('status', UNDEFINED))
        message = _import_ns.get('message', context.get('message', UNDEFINED))
        def render_msg(msg,status='done'):
            return render_render_msg(context,msg,status)
        __M_writer = context.writer()
        __M_writer(u'\n    ')
        __M_writer(unicode(render_msg( message, status )))
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "ascii", "line_map": {"133": 28, "139": 31, "16": 1, "167": 46, "147": 31, "148": 32, "149": 32, "150": 33, "151": 33, "157": 46, "39": 18, "168": 47, "169": 47, "45": 0, "175": 169, "53": 15, "54": 16, "55": 18, "56": 20, "60": 20, "61": 29, "62": 40, "63": 45, "64": 48, "65": 52, "66": 65, "72": 50, "82": 50, "83": 51, "84": 51, "90": 55, "97": 55, "98": 56, "107": 63, "108": 64, "109": 64, "110": 64, "111": 64, "117": 22, "125": 22, "126": 23}, "uri": "/message.mako", "filename": "templates/message.mako"}
__M_END_METADATA
"""
