# -*- coding:ascii -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1568315405.147572
_enable_loop = True
_template_filename = u'templates/webapps/tool_shed/common/common.mako'
_template_uri = u'/webapps/tool_shed/common/common.mako'
_source_encoding = 'ascii'
_exports = ['render_review_comment', 'render_select', 'render_deprecated_repository_dependencies_message', 'render_checkbox', 'render_long_description', 'render_star_rating', 'common_misc_javascripts', 'render_multiple_heads_message']


def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        __M_writer = context.writer()
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


def render_render_review_comment(context,comment_text):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer(u'\n    <style type="text/css">\n        #reviews_table{ table-layout:fixed;\n                        width:100%;\n                        overflow-wrap:normal;\n                        overflow:hidden;\n                        border:0px; \n                        word-break:keep-all;\n                        word-wrap:break-word;\n                        line-break:strict; }\n    </style>\n    <table id="reviews_table">\n        <tr><td>')
        __M_writer(unicode(comment_text))
        __M_writer(u'</td></tr>\n    </table>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_render_select(context,select):
    __M_caller = context.caller_stack._push_frame()
    try:
        disabled = context.get('disabled', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n    ')
        from markupsafe import escape 
        
        __M_writer(u'\n    ')
        from galaxy.util import listify 
        
        __M_writer(u'\n')
        if select.display == "checkboxes":
            for o in select.options:
                __M_writer(u'            <div>\n                ')
                selected = o[1] in listify(select.value) or o[2] 
                
                __M_writer(u'\n                <input type="checkbox" name="')
                __M_writer(unicode(select.name))
                __M_writer(u'" value="')
                __M_writer(unicode(escape(o[1])))
                __M_writer(u'"\n                ')
                __M_writer(unicode("refresh_on_change='true'" if select.refresh_on_change else ""))
                __M_writer(u'"\n                ')
                __M_writer(unicode("checked" if selected else ""))
                __M_writer(u' ')
                __M_writer(unicode("disabled" if disabled else ""))
                __M_writer(u'>\n                ')
                __M_writer(unicode(escape(o[0])))
                __M_writer(u'\n            </div>\n')
        else:
            __M_writer(u'        <select id="')
            __M_writer(unicode(select.field_id))
            __M_writer(u'" name="')
            __M_writer(unicode(select.name))
            __M_writer(u'"\n            ')
            __M_writer(unicode("multiple" if select.multiple else ""))
            __M_writer(u'\n            ')
            __M_writer(unicode("refresh_on_change='true'" if select.refresh_on_change else ""))
            __M_writer(u'">\n')
            for o in select.options:
                __M_writer(u'                ')
                selected = o[1] in listify(select.value) or o[2] 
                
                __M_writer(u'\n                <option value="')
                __M_writer(unicode(escape(o[1])))
                __M_writer(u'" ')
                __M_writer(unicode("selected" if selected else ""))
                __M_writer(u'>')
                __M_writer(unicode(escape(o[0])))
                __M_writer(u'</option>\n')
            __M_writer(u'        </select>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_render_deprecated_repository_dependencies_message(context,deprecated_repository_dependency_tups):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer(u'\n    <div class="warningmessage">\n        ')

        from tool_shed.util.common_util import parse_repository_dependency_tuple
        msg = '<ul>'
        for deprecated_repository_dependency_tup in deprecated_repository_dependency_tups:
            toolshed, name, owner, changeset_revision, pir, oicct = \
                parse_repository_dependency_tuple( deprecated_repository_dependency_tup )
            msg += '<li>Revision <b>%s</b> of repository <b>%s</b> owned by <b>%s</b></li>' % \
                    ( changeset_revision, name, owner )
        msg += '</ul>'
                
        
        __M_writer(u'\n        This repository depends upon the following deprecated repositories<br/>\n        ')
        __M_writer(unicode(msg))
        __M_writer(u'\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_render_checkbox(context,checkbox,disabled=False,refresh_on_change=False):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer(u'\n    ')
        from galaxy.web.form_builder import CheckboxField 
        
        __M_writer(u'\n    <input type="checkbox" id="')
        __M_writer(unicode(checkbox.name))
        __M_writer(u'" name="')
        __M_writer(unicode(checkbox.name))
        __M_writer(u'" value="true"\n        ')
        __M_writer(unicode("refresh_on_change='true'" if refresh_on_change else ""))
        __M_writer(u'\n        ')
        __M_writer(unicode("checked" if CheckboxField.is_checked(checkbox.value) else ""))
        __M_writer(u'\n        ')
        __M_writer(unicode("disabled" if disabled else ""))
        __M_writer(u'\n    >\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_render_long_description(context,description_text):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer(u'\n    <style type="text/css">\n        #description_table{ table-layout:fixed;\n                            width:100%;\n                            overflow-wrap:normal;\n                            overflow:hidden;\n                            border:0px; \n                            word-break:keep-all;\n                            word-wrap:break-word;\n                            line-break:strict; }\n    </style>\n    <div class="form-row">\n        <label>Detailed description:</label>\n        <table id="description_table">\n            <tr><td>')
        __M_writer(unicode(description_text))
        __M_writer(u'</td></tr>\n        </table>\n        <div style="clear: both"></div>\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_render_star_rating(context,name,rating,disabled=False):
    __M_caller = context.caller_stack._push_frame()
    try:
        range = context.get('range', UNDEFINED)
        str = context.get('str', UNDEFINED)
        __M_writer = context.writer()
        __M_writer(u'\n    ')

        if disabled:
            disabled_str = ' disabled="disabled"'
        else:
            disabled_str = ''
        html = ''
        for index in range( 1, 6 ):
            html += '<input name="%s" type="radio" class="star" value="%s" %s' % ( str( name ), str( index ), disabled_str )
            if rating > ( index - 0.5 ) and rating < ( index + 0.5 ):
                html += ' checked="checked"'
            html += '/>'
            
        
        __M_writer(u'\n    ')
        __M_writer(unicode(html))
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_common_misc_javascripts(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer(u'\n    <script type="text/javascript">\n        function checkAllFields( chkAll, name )\n        {\n            var checks = document.getElementsByTagName( \'input\' );\n            var boxLength = checks.length;\n            var allChecked = false;\n            var totalChecked = 0;\n            if ( chkAll.checked == true )\n            {\n                for ( i=0; i < boxLength; i++ )\n                {\n                    if ( checks[ i ].name.indexOf( name ) != -1 )\n                    {\n                       checks[ i ].checked = true;\n                    }\n                }\n            }\n            else\n            {\n                for ( i=0; i < boxLength; i++ )\n                {\n                    if ( checks[ i ].name.indexOf( name ) != -1 )\n                    {\n                       checks[ i ].checked = false;\n                    }\n                }\n            }\n        }\n\n        function checkAllRepositoryIdFields()\n        {\n            var chkAll = document.getElementById( \'checkAll\' );\n            var name = \'repository_ids\';\n            checkAllFields( chkAll, name );\n        }\n\n        function checkAllInstalledToolDependencyIdFields()\n        {\n            var chkAll = document.getElementById( \'checkAllInstalled\' );\n            var name = \'inst_td_ids\';\n            checkAllFields( chkAll, name );\n        }\n\n        function checkAllUninstalledToolDependencyIdFields()\n        {\n            var chkAll = document.getElementById( \'checkAllUninstalled\' );\n            var name = \'uninstalled_tool_dependency_ids\';\n            checkAllFields( chkAll, name );\n        }\n    </script>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_render_multiple_heads_message(context,heads):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        __M_writer(u'\n    <div class="warningmessage">\n        ')

        from tool_shed.util.hg_util import get_revision_label_from_ctx
        heads_str = ''
        for ctx in heads:
            heads_str += '%s<br/>' % get_revision_label_from_ctx( ctx, include_date=True )
                
        
        __M_writer(u'\n        Contact the administrator of this Tool Shed as soon as possible and let them know that\n        this repository has the following multiple heads which must be merged.<br/>\n        ')
        __M_writer(unicode(heads_str))
        __M_writer(u'\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "ascii", "line_map": {"16": 0, "21": 8, "22": 33, "23": 86, "24": 103, "25": 119, "26": 139, "27": 153, "28": 169, "34": 155, "38": 155, "39": 167, "40": 167, "46": 10, "51": 10, "52": 11, "54": 11, "55": 12, "57": 12, "58": 13, "59": 14, "60": 15, "61": 16, "63": 16, "64": 17, "65": 17, "66": 17, "67": 17, "68": 18, "69": 18, "70": 19, "71": 19, "72": 19, "73": 19, "74": 20, "75": 20, "76": 23, "77": 24, "78": 24, "79": 24, "80": 24, "81": 24, "82": 25, "83": 25, "84": 26, "85": 26, "86": 27, "87": 28, "88": 28, "90": 28, "91": 29, "92": 29, "93": 29, "94": 29, "95": 29, "96": 29, "97": 31, "103": 88, "107": 88, "108": 90, "119": 99, "120": 101, "121": 101, "127": 1, "131": 1, "132": 2, "134": 2, "135": 3, "136": 3, "137": 3, "138": 3, "139": 4, "140": 4, "141": 5, "142": 5, "143": 6, "144": 6, "150": 121, "154": 121, "155": 135, "156": 135, "162": 105, "168": 105, "169": 106, "182": 117, "183": 118, "184": 118, "190": 35, "194": 35, "200": 141, "204": 141, "205": 143, "212": 148, "213": 151, "214": 151, "220": 214}, "uri": "/webapps/tool_shed/common/common.mako", "filename": "templates/webapps/tool_shed/common/common.mako"}
__M_END_METADATA
"""
