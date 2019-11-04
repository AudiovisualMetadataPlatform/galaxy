# -*- coding:ascii -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1568307820.46636
_enable_loop = True
_template_filename = u'templates/galaxy_client_app.mako'
_template_uri = u'/galaxy_client_app.mako'
_source_encoding = 'ascii'
_exports = ['load', 'render_json', 'get_user_dict', 'get_user_json', 'get_config_json', 'get_config_dict']


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
        __M_writer(u'\n\n')
        __M_writer(u'\n')
        __M_writer(u'\n\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_load(context,app=None,**kwargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)
        def render_json(dictionary):
            return render_render_json(context,dictionary)
        trans = context.get('trans', UNDEFINED)
        def get_user_dict():
            return render_get_user_dict(context)
        def get_config_dict():
            return render_get_config_dict(context)
        __M_writer = context.writer()
        __M_writer(u'\n    <script type="text/javascript">\n\n        var bootstrapped = {};\n')
        for key in kwargs:
            __M_writer(u"            bootstrapped[ '")
            __M_writer(unicode(key))
            __M_writer(u"' ] = (\n                ")
            __M_writer(unicode( render_json( kwargs[ key ] ) ))
            __M_writer(u'\n            );\n')
        __M_writer(u"\n        var options = {\n            root: '")
        __M_writer(unicode(h.url_for( "/" )))
        __M_writer(u"',\n            config: ")
        __M_writer(unicode( render_json( get_config_dict() )))
        __M_writer(u',\n            user: ')
        __M_writer(unicode( render_json( get_user_dict() )))
        __M_writer(u",\n            session_csrf_token: '")
        __M_writer(unicode( trans.session_csrf_token ))
        __M_writer(u"'\n        };\n\n        window.bundleEntries.setGalaxyInstance(function(GalaxyApp) {\n            return new GalaxyApp(options, bootstrapped);\n        });\n\n")
        if app:
            __M_writer(u'            console.warn("Does app ever run? Is it ever not-named app?");\n            require([ \'')
            __M_writer(unicode(app))
            __M_writer(u"' ]);\n")
        __M_writer(u'        \n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_render_json(context,dictionary):
    __M_caller = context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)
        trans = context.get('trans', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n')
        __M_writer(unicode( h.dumps( dictionary, indent=( 2 if trans.debug else 0 ) ) ))
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_get_user_dict(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        AssertionError = context.get('AssertionError', UNDEFINED)
        Exception = context.get('Exception', UNDEFINED)
        int = context.get('int', UNDEFINED)
        float = context.get('float', UNDEFINED)
        util = context.get('util', UNDEFINED)
        trans = context.get('trans', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n')
        __M_writer(u'    ')

        from markupsafe import escape
        user_dict = {}
        try:
            if trans.user:
                user_dict = trans.user.to_dict( view='element',
                    value_mapper={ 'id': trans.security.encode_id, 'total_disk_usage': float, 'email': escape, 'username': escape } )
                user_dict[ 'quota_percent' ] = trans.app.quota_agent.get_percent( trans=trans )
                user_dict[ 'is_admin' ] = trans.user_is_admin
        
                # tags used
                users_api_controller = trans.webapp.api_controllers[ 'users' ]
                tags_used = []
                for tag in users_api_controller.get_user_tags_used( trans, user=trans.user ):
                    tag = escape( tag )
                    if tag:
                        tags_used.append( tag )
                user_dict[ 'tags_used' ] = tags_used
        
                return user_dict
        
            usage = 0
            percent = None
            try:
                usage = trans.app.quota_agent.get_usage( trans, history=trans.history )
                percent = trans.app.quota_agent.get_percent( trans=trans, usage=usage )
            except AssertionError as assertion:
                # no history for quota_agent.get_usage assertion
                pass
            return {
                'total_disk_usage'      : int( usage ),
                'nice_total_disk_usage' : util.nice_size( usage ),
                'quota_percent'         : percent
            }
        
        except Exception as exc:
            pass
            #TODO: no logging available?
            #log.exception( exc )
        
        return user_dict
            
        
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_get_user_json(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)
        def get_user_dict():
            return render_get_user_dict(context)
        __M_writer = context.writer()
        __M_writer(u'\n')
        __M_writer(unicode( h.dumps( get_user_dict() )))
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_get_config_json(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)
        def get_config_dict():
            return render_get_config_dict(context)
        __M_writer = context.writer()
        __M_writer(u'\n')
        __M_writer(unicode( h.dumps( get_config_dict() )))
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_get_config_dict(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        Exception = context.get('Exception', UNDEFINED)
        trans = context.get('trans', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n')
        __M_writer(u'    ')

        config_dict = {}
        try:
            controller = trans.webapp.api_controllers.get( 'configuration', None )
            if controller:
                config_dict = controller.get_config_dict( trans, trans.user_is_admin )
        except Exception as exc:
            pass
        return config_dict
            
        
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "ascii", "line_map": {"140": 103, "16": 0, "146": 106, "21": 3, "22": 6, "23": 34, "24": 50, "25": 55, "26": 104, "27": 109, "154": 108, "33": 7, "155": 108, "168": 52, "169": 54, "170": 54, "176": 38, "45": 7, "46": 11, "47": 12, "48": 12, "49": 12, "50": 13, "51": 13, "52": 16, "53": 18, "54": 18, "55": 19, "56": 19, "57": 20, "58": 20, "59": 21, "60": 21, "61": 28, "62": 29, "63": 30, "64": 30, "65": 32, "195": 49, "182": 38, "71": 1, "201": 195, "183": 40, "77": 1, "78": 2, "79": 2, "184": 40, "85": 59, "95": 59, "96": 62, "97": 62, "161": 52, "153": 106}, "uri": "/galaxy_client_app.mako", "filename": "templates/galaxy_client_app.mako"}
__M_END_METADATA
"""
