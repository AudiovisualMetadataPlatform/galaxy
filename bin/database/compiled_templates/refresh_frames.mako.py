# -*- coding:ascii -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1568307820.44703
_enable_loop = True
_template_filename = u'templates/refresh_frames.mako'
_template_uri = u'/refresh_frames.mako'
_source_encoding = 'ascii'
_exports = ['handle_refresh_frames']


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_handle_refresh_frames(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        int = context.get('int', UNDEFINED)
        h = context.get('h', UNDEFINED)
        app = context.get('app', UNDEFINED)
        trans = context.get('trans', UNDEFINED)
        refresh_frames = context.get('refresh_frames', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n')
        __M_writer(u'    ')

        if not refresh_frames: return ''
            
        
        __M_writer(u'\n\n')
        __M_writer(u'    <script type="text/javascript">\n        function user_changed( user_email, is_admin ) {\n            if ( user_email ) {\n                $(".loggedin-only").show();\n                $(".loggedout-only").hide();\n                $("#user-email").text( user_email );\n                if ( is_admin ) {\n                    $(".admin-only").show();\n                }\n            } else {\n                $(".loggedin-only").hide();\n                $(".loggedout-only").show();\n                $(".admin-only").hide();\n            }\n        }\n\n')
        if 'everything' in refresh_frames:
            __M_writer(u'        parent.location.href="')
            __M_writer(unicode(h.url_for( controller='root' )))
            __M_writer(u'";\n')
        if 'masthead' in refresh_frames:
            __M_writer(u'\n')
            __M_writer(u'        if ( parent.user_changed ) {\n')
            if trans.user:
                __M_writer(u'                parent.user_changed( "')
                __M_writer(filters.html_escape(unicode(trans.user.email )))
                __M_writer(u'", ')
                __M_writer(unicode(int( app.config.is_admin_user( trans.user ) )))
                __M_writer(u' );\n')
            else:
                __M_writer(u'                parent.user_changed( null, false );\n')
            __M_writer(u'        }\n')
        if 'history' in refresh_frames:
            __M_writer(u'        if( top.Galaxy && top.Galaxy.currHistoryPanel ){\n            top.Galaxy.currHistoryPanel.loadCurrentHistory();\n        }\n')
        if 'tools' in refresh_frames:
            __M_writer(u"        if ( parent.frames && Galaxy.toolPanel ) {\n            // FIXME: refreshing the tool menu does not work with new JS-based approach,\n            // but refreshing the tool menu is not used right now, either.\n\n            if ( parent.force_left_panel ) {\n                parent.force_left_panel( 'show' );\n            }\n        }\n")
        __M_writer(u'    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "ascii", "line_map": {"16": 0, "21": 61, "27": 2, "36": 2, "37": 4, "38": 4, "42": 6, "43": 9, "44": 25, "45": 26, "46": 26, "47": 26, "48": 28, "49": 35, "50": 37, "51": 38, "52": 39, "53": 39, "54": 39, "55": 39, "56": 39, "57": 40, "58": 41, "59": 43, "60": 45, "61": 46, "62": 50, "63": 51, "64": 60, "70": 64}, "uri": "/refresh_frames.mako", "filename": "templates/refresh_frames.mako"}
__M_END_METADATA
"""
