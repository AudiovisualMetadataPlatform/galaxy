# -*- coding:ascii -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1568315405.180064
_enable_loop = True
_template_filename = u'templates/base/base_panels.mako'
_template_uri = u'/base/base_panels.mako'
_source_encoding = 'ascii'
_exports = ['overlay', 'late_javascripts', 'stylesheets', 'init', 'javascript_app', 'masthead', 'javascripts']


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
        trans = context.get('trans', UNDEFINED)
        app = context.get('app', UNDEFINED)
        hasattr = context.get('hasattr', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'<!DOCTYPE HTML>\n')
        __M_writer(u'\n\n')

        self.has_left_panel = hasattr( self, 'left_panel' )
        self.has_right_panel = hasattr( self, 'right_panel' )
        self.message_box_visible = app.config.message_box_visible
        self.show_inactivity_warning = False
        if trans.webapp.name == 'galaxy' and trans.user:
            self.show_inactivity_warning = ( ( trans.user.active is False ) and ( app.config.user_activation_on ) )
        self.overlay_visible=False
        self.active_view=None
        self.body_class=""
        self.require_javascript=False
        
        
        __M_locals_builtin_stored = __M_locals_builtin()
        __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in [] if __M_key in __M_locals_builtin_stored]))
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'<html>\n    <!--base_panels.mako-->\n    ')
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
        __M_writer(unicode(self.stylesheets()))
        __M_writer(u'\n        ')
        __M_writer(unicode(self.javascripts()))
        __M_writer(u'\n        ')
        __M_writer(unicode(self.javascript_app()))
        __M_writer(u'\n    </head>\n\n    ')

        body_class = self.body_class
        if self.message_box_visible:
            body_class += " has-message-box"
        if self.show_inactivity_warning:
            body_class += " has-inactivity-box"
        
        
        __M_locals_builtin_stored = __M_locals_builtin()
        __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['body_class'] if __M_key in __M_locals_builtin_stored]))
        __M_writer(u'\n\n\n    <body scroll="no" class="full-content ')
        __M_writer(unicode(body_class))
        __M_writer(u'">\n')
        if self.require_javascript:
            __M_writer(u'            <noscript>\n                <div class="overlay overlay-background">\n                    <div class="modal dialog-box" border="0">\n                        <div class="modal-header"><h3 class="title">Javascript Required</h3></div>\n                        <div class="modal-body">The Galaxy analysis interface requires a browser with Javascript enabled. <br> Please enable Javascript and refresh this page</div>\n                    </div>\n                </div>\n            </noscript>\n')
        __M_writer(u'        <div id="everything" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;">\n')
        __M_writer(u'            <div id="background"></div>\n')
        __M_writer(u'            <div id="masthead" class="navbar navbar-fixed-top navbar-inverse">\n                ')
        __M_writer(unicode(self.masthead()))
        __M_writer(u'\n            </div>\n')
        if self.message_box_visible:
            __M_writer(u'                <div id="messagebox" class="panel-')
            __M_writer(unicode(app.config.message_box_class))
            __M_writer(u'-message" style="display:block">\n                    ')
            __M_writer(unicode(app.config.message_box_content))
            __M_writer(u'\n                </div>\n')
        if self.show_inactivity_warning:
            __M_writer(u'                <div id="inactivebox" class="panel-warning-message">\n                    ')
            __M_writer(unicode(app.config.inactivity_box_content))
            __M_writer(u' <a href="')
            __M_writer(unicode(h.url_for( controller='user', action='resend_verification' )))
            __M_writer(u'">Resend verification.</a>\n                </div>\n')
        __M_writer(u'            ')
        __M_writer(unicode(self.overlay(visible=self.overlay_visible)))
        __M_writer(u'\n            <div id="columns">\n')
        if self.has_left_panel:
            __M_writer(u'                    <div id="left">\n                        ')
            __M_writer(unicode(self.left_panel()))
            __M_writer(u'\n                        <div class="unified-panel-footer">\n                            <div id="left-panel-collapse" class="panel-collapse"></div>\n                            <div id="left-panel-drag" class="drag"></div>\n                        </div>\n                    </div><!--end left-->\n')
        __M_writer(u'                <div id="center" class="inbound">\n                    ')
        __M_writer(unicode(self.center_panel()))
        __M_writer(u'\n                </div><!--end center-->\n')
        if self.has_right_panel:
            __M_writer(u'                    <div id="right">\n                        ')
            __M_writer(unicode(self.right_panel()))
            __M_writer(u'\n                        <div class="unified-panel-footer">\n                            <div id="right-panel-collapse" class="panel-collapse right"></div>\n                            <div id="right-panel-drag" class="drag"></div>\n                        </div>\n                    </div><!--end right-->\n')
        __M_writer(u'            </div><!--end columns-->\n        </div><!--end everything-->\n        <div id=\'dd-helper\' style="display: none;"></div>\n')
        __M_writer(u'        ')
        __M_writer(unicode(self.late_javascripts()))
        __M_writer(u'\n    </body>\n</html>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_overlay(context,title='',content='',visible=False):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer(u'\n    ')
        __M_writer(u'\n    ')
        __M_writer(u'\n\n    ')

        if visible:
            display = "style='display: block;'"
            overlay_class = "in"
        else:
            display = "style='display: none;'"
            overlay_class = ""
        
        
        __M_writer(u'\n\n    <div id="top-modal" class="modal ')
        __M_writer(unicode(overlay_class))
        __M_writer(u'" ')
        __M_writer(unicode(display))
        __M_writer(u'>\n        <div id="top-modal-backdrop" class="modal-backdrop fade ')
        __M_writer(unicode(overlay_class))
        __M_writer(u'" style="z-index: -1"></div>\n        <div id="top-modal-dialog" class="modal-dialog">\n            <div class="modal-content">\n                <div class="modal-header">\n                    <button type=\'button\' class=\'close\' style="display: none;">&times;</button>\n                    <h4 class=\'title\'>')
        __M_writer(unicode(title))
        __M_writer(u'</h4>\n                </div>\n                <div class="modal-body">')
        __M_writer(unicode(content))
        __M_writer(u'</div>\n                <div class="modal-footer">\n                    <div class="buttons" style="float: right;"></div>\n                    <div class="extra_buttons" style=""></div>\n                    <div style="clear: both;"></div>\n                </div>\n            </div>\n        </div>\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_late_javascripts(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        self = context.get('self', UNDEFINED)
        app = context.get('app', UNDEFINED)
        t = context.get('t', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n')
        __M_writer(u'    <script type="text/javascript">\n\n')
        if self.has_left_panel:
            __M_writer(u"        var lp = new panels.LeftPanel({ el: '#left' });\n        window.force_left_panel = function( x ) { lp.force_panel( x ) };\n")
        __M_writer(u'\n')
        if self.has_right_panel:
            __M_writer(u"        var rp = new panels.RightPanel({ el: '#right' });\n        window.handle_minwidth_hint = function( x ) { rp.handle_minwidth_hint( x ) };\n        window.force_right_panel = function( x ) { rp.force_panel( x ) };\n")
        __M_writer(u'\n')
        if t.webapp.name == 'galaxy' and app.config.ga_code:
            __M_writer(u"          (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){\n          (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),\n          m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)\n          })(window,document,'script','//www.google-analytics.com/analytics.js','ga');\n          ga('create', '")
            __M_writer(unicode(app.config.ga_code))
            __M_writer(u"', 'auto');\n          ga('send', 'pageview');\n")
        __M_writer(u'\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_stylesheets(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        h = context.get('h', UNDEFINED)
        self = context.get('self', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n    ')
        __M_writer(unicode(h.css(
        'jquery.rating',
        'bootstrap-tour',
        'base'
    )))
        __M_writer(u'\n    <style type="text/css">\n    #center {\n')
        if not self.has_left_panel:
            __M_writer(u'            left: 0 !important;\n')
        if not self.has_right_panel:
            __M_writer(u'            right: 0 !important;\n')
        __M_writer(u'    }\n    </style>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_init(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_javascript_app(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        galaxy_client = _mako_get_namespace(context, 'galaxy_client')
        __M_writer = context.writer()
        __M_writer(u'\n')
        __M_writer(u'    ')
        __M_writer(unicode( galaxy_client.load() ))
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_masthead(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
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
                __M_writer(filters.html_escape(unicode(trans.user.email )))
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
        __M_writer(u'\n    \n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "ascii", "line_map": {"23": 2, "26": 0, "36": 1, "37": 2, "38": 4, "53": 15, "54": 19, "55": 38, "56": 61, "57": 66, "58": 95, "59": 100, "60": 132, "61": 135, "62": 137, "63": 137, "64": 141, "65": 143, "66": 147, "67": 148, "68": 148, "69": 148, "70": 150, "71": 150, "72": 150, "73": 153, "74": 153, "75": 153, "76": 154, "77": 154, "78": 155, "79": 155, "80": 156, "81": 156, "82": 159, "92": 165, "93": 168, "94": 168, "95": 169, "96": 170, "97": 179, "98": 181, "99": 183, "100": 184, "101": 184, "102": 186, "103": 187, "104": 187, "105": 187, "106": 188, "107": 188, "108": 191, "109": 192, "110": 193, "111": 193, "112": 193, "113": 193, "114": 196, "115": 196, "116": 196, "117": 198, "118": 199, "119": 200, "120": 200, "121": 207, "122": 208, "123": 208, "124": 210, "125": 211, "126": 212, "127": 212, "128": 219, "129": 225, "130": 225, "131": 225, "137": 102, "141": 102, "142": 103, "143": 104, "144": 106, "153": 113, "154": 115, "155": 115, "156": 115, "157": 115, "158": 116, "159": 116, "160": 121, "161": 121, "162": 123, "163": 123, "169": 69, "176": 69, "177": 72, "178": 74, "179": 75, "180": 78, "181": 79, "182": 80, "183": 84, "184": 85, "185": 86, "186": 90, "187": 90, "188": 93, "194": 22, "200": 22, "201": 23, "206": 27, "207": 30, "208": 31, "209": 33, "210": 34, "211": 36, "217": 17, "221": 17, "227": 63, "232": 63, "233": 65, "234": 65, "235": 65, "241": 98, "245": 98, "251": 41, "258": 41, "259": 43, "260": 44, "261": 44, "262": 44, "263": 46, "264": 46, "265": 47, "266": 48, "267": 48, "268": 48, "269": 50, "270": 52, "271": 53, "278": 59, "284": 278}, "uri": "/base/base_panels.mako", "filename": "templates/base/base_panels.mako"}
__M_END_METADATA
"""
