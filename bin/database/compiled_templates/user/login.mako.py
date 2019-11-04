# -*- coding:ascii -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1568307820.425046
_enable_loop = True
_template_filename = 'templates/user/login.mako'
_template_uri = '/user/login.mako'
_source_encoding = 'ascii'
_exports = ['body', 'render_openid_form', 'center_panel', 'render_oidc_form', 'init', 'render_login_form']



#This is a hack, we should restructure templates to avoid this.
def inherit(context):
    if context.get('trans').webapp.name == 'galaxy' and context.get( 'use_panels', True ):
        return '/webapps/galaxy/base_panels.mako'
    elif context.get('trans').webapp.name == 'tool_shed' and context.get( 'use_panels', True ):
        return '/webapps/tool_shed/base_panels.mako'
    else:
        return '/base.mako'


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    ns = runtime.TemplateNamespace('__anon_0x13781cc90', context._clean_inheritance_tokens(), templateuri=u'/message.mako', callables=None,  calling_uri=_template_uri)
    context.namespaces[(__name__, '__anon_0x13781cc90')] = ns

def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, (inherit(context)), _template_uri)
def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x13781cc90')._populate(_import_ns, [u'render_msg'])
        __M_writer = context.writer()
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
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
        _mako_get_namespace(context, '__anon_0x13781cc90')._populate(_import_ns, [u'render_msg'])
        status = _import_ns.get('status', context.get('status', UNDEFINED))
        redirect = _import_ns.get('redirect', context.get('redirect', UNDEFINED))
        render_msg = _import_ns.get('render_msg', context.get('render_msg', UNDEFINED))
        redirect_url = _import_ns.get('redirect_url', context.get('redirect_url', UNDEFINED))
        def render_openid_form(redirect,auto_associate,openid_providers):
            return render_render_openid_form(context,redirect,auto_associate,openid_providers)
        def render_oidc_form(form_action=None):
            return render_render_oidc_form(context,form_action)
        def render_login_form(form_action=None):
            return render_render_login_form(context,form_action)
        openid_providers = _import_ns.get('openid_providers', context.get('openid_providers', UNDEFINED))
        message = _import_ns.get('message', context.get('message', UNDEFINED))
        trans = _import_ns.get('trans', context.get('trans', UNDEFINED))
        hasattr = _import_ns.get('hasattr', context.get('hasattr', UNDEFINED))
        __M_writer = context.writer()
        __M_writer(u'\n\n')
        if redirect_url:
            __M_writer(u'        <script type="text/javascript">  \n            top.location.href = \'')
            __M_writer(filters.html_escape(unicode(redirect_url )))
            __M_writer(u"';\n        </script>\n")
        __M_writer(u'\n')
        if context.get('use_panels'):
            __M_writer(u'        <div style="margin: 1em;">\n')
        else:
            __M_writer(u'        <div>\n')
        __M_writer(u'\n')
        if message:
            __M_writer(u'        ')
            __M_writer(unicode(render_msg( message, status )))
            __M_writer(u'\n')
        __M_writer(u'\n')
        if not trans.user:
            __M_writer(u'\n        ')
            __M_writer(unicode(render_login_form()))
            __M_writer(u'\n\n        <br/>\n')
            if hasattr(trans.app.config, 'enable_oidc') and trans.app.config.enable_oidc:
                __M_writer(u'            <br/>\n            ')
                __M_writer(unicode(render_oidc_form()))
                __M_writer(u'\n')
            __M_writer(u'\n')
            if trans.app.config.enable_openid:
                __M_writer(u'            <br/>\n            ')
                __M_writer(unicode(render_openid_form( redirect, False, openid_providers )))
                __M_writer(u'\n')
            __M_writer(u'\n')
            if trans.app.config.get( 'terms_url', None ) is not None:
                __M_writer(u'            <br/>\n            <p>\n                <a href="')
                __M_writer(unicode(trans.app.config.get('terms_url', None)))
                __M_writer(u'">Terms and Conditions for use of this service</a>\n            </p>\n')
            __M_writer(u'\n')
        __M_writer(u'\n    </div>\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_render_openid_form(context,redirect,auto_associate,openid_providers):
    __M_caller = context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x13781cc90')._populate(_import_ns, [u'render_msg'])
        h = _import_ns.get('h', context.get('h', UNDEFINED))
        __M_writer = context.writer()
        __M_writer(u'\n    <div class="card">\n        <div class="card-header">OpenID Login</div>\n        <form name="openid" id="openid" action="')
        __M_writer(unicode(h.url_for( controller='user', action='openid_auth' )))
        __M_writer(u'" method="post" target="_parent" >\n            <div class="form-row">\n                <label>OpenID URL:</label>\n                <input type="text" name="openid_url" size="60" style="background-image:url(\'')
        __M_writer(unicode(h.url_for( '/static/images/openid-16x16.gif' )))
        __M_writer(u'\' ); background-repeat: no-repeat; padding-right: 20px; background-position: 99% 50%;"/>\n                <input type="hidden" name="redirect" value="')
        __M_writer(filters.html_escape(unicode(redirect )))
        __M_writer(u'" size="40"/>\n            </div>\n            <div class="form-row">\n                Or, authenticate with your <select name="openid_provider">\n')
        for provider in openid_providers:
            __M_writer(u'                    <option value="')
            __M_writer(unicode(provider.id))
            __M_writer(u'">')
            __M_writer(unicode(provider.name))
            __M_writer(u'</option>\n')
        __M_writer(u'                </select> account.\n            </div>\n            <div class="form-row">\n                <input type="submit" name="login_button" value="Login"/>\n            </div>\n        </form>\n    </div>\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_center_panel(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x13781cc90')._populate(_import_ns, [u'render_msg'])
        def body():
            return render_body(context)
        __M_writer = context.writer()
        __M_writer(u'\n    ')
        __M_writer(unicode(body()))
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_render_oidc_form(context,form_action=None):
    __M_caller = context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x13781cc90')._populate(_import_ns, [u'render_msg'])
        h = _import_ns.get('h', context.get('h', UNDEFINED))
        header = _import_ns.get('header', context.get('header', UNDEFINED))
        __M_writer = context.writer()
        __M_writer(u'\n\n    ')

        if form_action is None:
            form_action = h.url_for( controller='authnz', action='login', provider='Google' )
            
        
        __M_writer(u'\n\n')
        if header:
            __M_writer(u'        ')
            __M_writer(unicode(header))
            __M_writer(u'\n')
        __M_writer(u'    <div class="card">\n        <div class="card-header">OR</div>\n        <form name="oidc" id="oidc" action="')
        __M_writer(unicode(form_action))
        __M_writer(u'" method="post" >\n            <div class="form-row">\n                <input type="submit" value="Login with Google"/>\n            </div>\n        </form>\n    </div>\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_init(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x13781cc90')._populate(_import_ns, [u'render_msg'])
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


def render_render_login_form(context,form_action=None):
    __M_caller = context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x13781cc90')._populate(_import_ns, [u'render_msg'])
        redirect = _import_ns.get('redirect', context.get('redirect', UNDEFINED))
        use_panels = _import_ns.get('use_panels', context.get('use_panels', UNDEFINED))
        h = _import_ns.get('h', context.get('h', UNDEFINED))
        header = _import_ns.get('header', context.get('header', UNDEFINED))
        login = _import_ns.get('login', context.get('login', UNDEFINED))
        trans = _import_ns.get('trans', context.get('trans', UNDEFINED))
        __M_writer = context.writer()
        __M_writer(u'\n\n    ')

        if form_action is None:
            form_action = h.url_for( controller='user', action='login', use_panels=use_panels )
            
        
        __M_writer(u'\n\n')
        if header:
            __M_writer(u'        ')
            __M_writer(unicode(header))
            __M_writer(u'\n')
        __M_writer(u'    <div class="card">\n        <div class="card-header">Login</div>\n        <form name="login" id="login" action="')
        __M_writer(unicode(form_action))
        __M_writer(u'" method="post" >\n            <input type="hidden" name="session_csrf_token" value="')
        __M_writer(unicode(trans.session_csrf_token))
        __M_writer(u'" />\n            <div class="form-row">\n                <label>Username / Email Address:</label>\n                <input type="text" name="login" value="')
        __M_writer(filters.html_escape(unicode(login or '')))
        __M_writer(u'" size="40"/>\n                <input type="hidden" name="redirect" value="')
        __M_writer(filters.html_escape(unicode(redirect )))
        __M_writer(u'" size="40"/>\n            </div>\n            <div class="form-row">\n                <label>Password:</label>\n                <input type="password" name="password" value="" size="40"/>\n                <div class="toolParamHelp" style="clear: both;">\n                    <a href="')
        __M_writer(unicode(h.url_for( controller='user', action='reset_password', use_panels=use_panels )))
        __M_writer(u'">Forgot password? Reset here</a>\n                </div>\n            </div>\n            <div class="form-row">\n                <input type="submit" name="login_button" value="Login"/>\n            </div>\n        </form>\n    </div>\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "ascii", "line_map": {"16": 1, "34": 23, "40": 0, "47": 10, "48": 12, "49": 21, "50": 23, "51": 27, "52": 73, "53": 107, "54": 128, "55": 152, "61": 29, "81": 29, "82": 31, "83": 32, "84": 33, "85": 33, "86": 36, "87": 37, "88": 38, "89": 39, "90": 40, "91": 42, "92": 43, "93": 44, "94": 44, "95": 44, "96": 46, "97": 47, "98": 48, "99": 49, "100": 49, "101": 52, "102": 53, "103": 54, "104": 54, "105": 56, "106": 57, "107": 58, "108": 59, "109": 59, "110": 61, "111": 62, "112": 63, "113": 65, "114": 65, "115": 68, "116": 70, "122": 130, "129": 130, "130": 133, "131": 133, "132": 136, "133": 136, "134": 137, "135": 137, "136": 141, "137": 142, "138": 142, "139": 142, "140": 142, "141": 142, "142": 144, "148": 25, "156": 25, "157": 26, "158": 26, "164": 109, "172": 109, "173": 111, "178": 114, "179": 116, "180": 117, "181": 117, "182": 117, "183": 119, "184": 121, "185": 121, "191": 14, "199": 14, "200": 15, "207": 20, "213": 75, "225": 75, "226": 77, "231": 80, "232": 82, "233": 83, "234": 83, "235": 83, "236": 85, "237": 87, "238": 87, "239": 88, "240": 88, "241": 91, "242": 91, "243": 92, "244": 92, "245": 98, "246": 98, "252": 246}, "uri": "/user/login.mako", "filename": "templates/user/login.mako"}
__M_END_METADATA
"""
