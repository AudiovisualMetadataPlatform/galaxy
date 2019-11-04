# -*- coding:ascii -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1568315473.015498
_enable_loop = True
_template_filename = 'templates/webapps/galaxy/workflow/editor.mako'
_template_uri = 'workflow/editor.mako'
_source_encoding = 'ascii'
_exports = ['left_panel', 'title', 'render_label', 'center_panel', 'overlay', 'render_module_section', 'stylesheets', 'init', 'right_panel', 'javascripts', 'render_tool']


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    ns = runtime.TemplateNamespace('__anon_0x1385f3a10', context._clean_inheritance_tokens(), templateuri=u'/tagging_common.mako', callables=None,  calling_uri=_template_uri)
    context.namespaces[(__name__, '__anon_0x1385f3a10')] = ns

def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'/webapps/galaxy/base_panels.mako', _template_uri)
def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x1385f3a10')._populate(_import_ns, [u'render_individual_tagging_element'])
        __M_writer = context.writer()
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_left_panel(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x1385f3a10')._populate(_import_ns, [u'render_individual_tagging_element'])
        trans = _import_ns.get('trans', context.get('trans', UNDEFINED))
        app = _import_ns.get('app', context.get('app', UNDEFINED))
        def render_label(label):
            return render_render_label(context,label)
        def render_module_section(module_section):
            return render_render_module_section(context,module_section)
        n_ = _import_ns.get('n_', context.get('n_', UNDEFINED))
        isinstance = _import_ns.get('isinstance', context.get('isinstance', UNDEFINED))
        def render_tool(tool,section):
            return render_render_tool(context,tool,section)
        __M_writer = context.writer()
        __M_writer(u'\n    ')

        from galaxy.tools import Tool
        from galaxy.tools.toolbox import ToolSection, ToolSectionLabel
            
        
        __M_writer(u'\n\n    <div class="unified-panel-header" unselectable="on">\n        <div class=\'unified-panel-header-inner\'>\n            ')
        __M_writer(unicode(n_('Tools')))
        __M_writer(u'\n        </div>\n    </div>\n\n    <div class="unified-panel-controls">\n        <div id="tool-search" class="bar">\n            <input id="tool-search-query" class="search-query parent-width" name="query" placeholder="search tools" autocomplete="off" type="text">\n             <a id="search-clear-btn" title="" data-original-title="clear search (esc)"> </a>\n             <span id="search-spinner" class="search-spinner fa fa-spinner fa-spin"></span>\n        </div>\n    </div>\n\n    <div class="unified-panel-body" style="overflow: auto;">\n        <div class="toolMenuContainer">\n            <div class="toolMenu" id="workflow-tool-menu">\n                ')

        from galaxy.workflow.modules import load_module_sections
        module_sections = load_module_sections( trans )
                        
        
        __M_writer(u'\n                <div class="toolSectionWrapper">\n                    ')
        __M_writer(unicode(render_module_section(module_sections['inputs'])))
        __M_writer(u'\n                </div>\n\n                <div class="toolSectionList">\n')
        for val in app.toolbox.tool_panel_contents( trans ):
            __M_writer(u'                        <div class="toolSectionWrapper">\n')
            if isinstance( val, Tool ):
                __M_writer(u'                            ')
                __M_writer(unicode(render_tool( val, False )))
                __M_writer(u'\n')
            elif isinstance( val, ToolSection ) and val.elems:
                __M_writer(u'                        ')
                section = val 
                
                __M_writer(u'\n                            <div class="toolSectionTitle" id="title_')
                __M_writer(unicode(section.id))
                __M_writer(u'">\n                                <span>')
                __M_writer(unicode(section.name))
                __M_writer(u'</span>\n                            </div>\n                            <div id="')
                __M_writer(unicode(section.id))
                __M_writer(u'" class="toolSectionBody">\n                                <div class="toolSectionBg">\n')
                for section_key, section_val in section.elems.items():
                    if isinstance( section_val, Tool ):
                        __M_writer(u'                                            ')
                        __M_writer(unicode(render_tool( section_val, True )))
                        __M_writer(u'\n')
                    elif isinstance( section_val, ToolSectionLabel ):
                        __M_writer(u'                                            ')
                        __M_writer(unicode(render_label( section_val )))
                        __M_writer(u'\n')
                __M_writer(u'                                </div>\n                            </div>\n')
            elif isinstance( val, ToolSectionLabel ):
                __M_writer(u'                            ')
                __M_writer(unicode(render_label( val )))
                __M_writer(u'\n')
            __M_writer(u'                        </div>\n')
        if trans.user_is_admin and trans.app.data_managers.data_managers:
            __M_writer(u'                       <div>&nbsp;</div>\n                       <div class="toolSectionWrapper">\n                           <div class="toolSectionTitle" id="title___DATA_MANAGER_TOOLS__">\n                               <span>Data Manager Tools</span>\n                           </div>\n                           <div id="__DATA_MANAGER_TOOLS__" class="toolSectionBody">\n                               <div class="toolSectionBg">\n')
            for data_manager_id, data_manager_val in trans.app.data_managers.data_managers.items():
                __M_writer(u'                                       ')
                __M_writer(unicode( render_tool( data_manager_val.tool, True ) ))
                __M_writer(u'\n')
            __M_writer(u'                               </div>\n                           </div>\n                       </div>\n')
        __M_writer(u'                </div>\n                <div>&nbsp;</div>\n')
        for section_name, module_section in module_sections.items():
            if section_name != "inputs":
                __M_writer(u'                        ')
                __M_writer(unicode(render_module_section(module_section)))
                __M_writer(u'\n')
        __M_writer(u'\n')
        __M_writer(u'                <div id="search-no-results" style="display: none; padding-top: 5px">\n                    <em><strong>Search did not match any tools.</strong></em>\n                </div>\n\n            </div>\n        </div>\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_title(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x1385f3a10')._populate(_import_ns, [u'render_individual_tagging_element'])
        __M_writer = context.writer()
        __M_writer(u'\n\n    Workflow Editor\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_render_label(context,label):
    __M_caller = context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x1385f3a10')._populate(_import_ns, [u'render_individual_tagging_element'])
        __M_writer = context.writer()
        __M_writer(u'\n    <div class="toolPanelLabel" id="title_')
        __M_writer(unicode(label.id))
        __M_writer(u'">\n        <span>')
        __M_writer(unicode(label.text))
        __M_writer(u'</span>\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_center_panel(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x1385f3a10')._populate(_import_ns, [u'render_individual_tagging_element'])
        h = _import_ns.get('h', context.get('h', UNDEFINED))
        stored = _import_ns.get('stored', context.get('stored', UNDEFINED))
        __M_writer = context.writer()
        __M_writer(u'\n\n    <div class="unified-panel-header" unselectable="on">\n        <div class="panel-header-buttons">\n            <a id="workflow-options-button" class="panel-header-button" href="#"><span class="fa fa-cog"></span></a>\n        </div>\n        <div class="unified-panel-header-inner">\n            ')
        __M_writer(filters.html_escape(unicode(h.to_unicode( stored.name ) )))
        __M_writer(u'\n        </div>\n    </div>\n    <div class="unified-panel-body" id="workflow-canvas-body">\n        <div id="canvas-viewport">\n            <div id="canvas-container" style="position: absolute; width: 100%; height: 100%;"></div>\n        </div>\n        <div id=\'workflow-parameters-box\' style="display:none; position: absolute; right:0px; border: solid grey 1px; padding: 5px; background: #EEEEEE; z-index: 20000; overflow: auto; max-width: 300px; max-height: 300px;">\n            <div style="margin-bottom:5px;">\n                <b>Workflow Parameters</b>\n            </div>\n            <div id="workflow-parameters-container">\n            </div>\n        </div>\n        <div class="workflow-overview">\n            <div style="position: relative; overflow: hidden; width: 100%; height: 100%; border-top: solid gray 1px; border-left: solid grey 1px;">\n                <div id="overview" style="position: absolute;">\n                    <canvas width="0" height="0" style="background: white; width: 100%; height: 100%;" id="overview-canvas"></canvas>\n                    <div id="overview-viewport" style="position: absolute; width: 0px; height: 0px; border: solid blue 1px; z-index: 10;"></div>\n                </div>\n            </div>\n        </div>\n    </div>\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_overlay(context,visible=False):
    __M_caller = context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x1385f3a10')._populate(_import_ns, [u'render_individual_tagging_element'])
        self = _import_ns.get('self', context.get('self', UNDEFINED))
        parent = _import_ns.get('parent', context.get('parent', UNDEFINED))
        __M_writer = context.writer()
        __M_writer(u'\n    ')
        __M_writer(unicode(parent.overlay( "Loading workflow editor...",
                      "<div class='progress progress-striped progress-info active'><div class='progress-bar' style='width: 100%;'></div></div>", self.overlay_visible )))
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_render_module_section(context,module_section):
    __M_caller = context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x1385f3a10')._populate(_import_ns, [u'render_individual_tagging_element'])
        __M_writer = context.writer()
        __M_writer(u'\n    <div class="toolSectionTitle" id="title___workflow__')
        __M_writer(unicode(module_section['name']))
        __M_writer(u'__">\n        <span>')
        __M_writer(unicode(module_section["title"]))
        __M_writer(u'</span>\n    </div>\n    <div id="__workflow__')
        __M_writer(unicode(module_section['name']))
        __M_writer(u'__" class="toolSectionBody">\n        <div class="toolSectionBg">\n')
        for module in module_section["modules"]:
            __M_writer(u'                <div class="toolTitle">\n                    <a href="#" id="tool-menu-')
            __M_writer(unicode(module_section['name']))
            __M_writer(u'-')
            __M_writer(unicode(module['name']))
            __M_writer(u'" onclick="workflow_globals.app.add_node_for_module( \'')
            __M_writer(unicode(module['name']))
            __M_writer(u"', '")
            __M_writer(unicode(module['title']))
            __M_writer(u'\' )">\n                        ')
            __M_writer(unicode(module['description']))
            __M_writer(u'\n                    </a>\n                </div>\n')
        __M_writer(u'        </div>\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_stylesheets(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x1385f3a10')._populate(_import_ns, [u'render_individual_tagging_element'])
        h = _import_ns.get('h', context.get('h', UNDEFINED))
        parent = _import_ns.get('parent', context.get('parent', UNDEFINED))
        __M_writer = context.writer()
        __M_writer(u'\n\n')
        __M_writer(u'    ')
        __M_writer(unicode(h.css( "base", "autocomplete_tagging", "jquery-ui/smoothness/jquery-ui" )))
        __M_writer(u'\n\n')
        __M_writer(u'    ')
        __M_writer(unicode(parent.stylesheets()))
        __M_writer(u'\n\n    <style type="text/css">\n    canvas { position: absolute; z-index: 10; }\n    canvas.dragging { position: absolute; z-index: 1000; }\n    </style>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_init(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x1385f3a10')._populate(_import_ns, [u'render_individual_tagging_element'])
        h = _import_ns.get('h', context.get('h', UNDEFINED))
        self = _import_ns.get('self', context.get('self', UNDEFINED))
        len = _import_ns.get('len', context.get('len', UNDEFINED))
        stored = _import_ns.get('stored', context.get('stored', UNDEFINED))
        workflows = _import_ns.get('workflows', context.get('workflows', UNDEFINED))
        trans = _import_ns.get('trans', context.get('trans', UNDEFINED))
        __M_writer = context.writer()
        __M_writer(u'\n')

        self.active_view="workflow"
        self.overlay_visible=True
        self.editor_config = {
            'id'      : trans.security.encode_id(stored.id),
            'urls'    : {
                'tool_search'         : h.url_for('/api/tools'),
                'get_datatypes'       : h.url_for('/api/datatypes/mapping'),
                'load_workflow'       : h.url_for(controller='workflow', action='load_workflow'),
                'run_workflow'        : h.url_for(controller='root', action='index', workflow_id=trans.security.encode_id(stored.id)),
                'rename_async'        : h.url_for(controller='workflow', action='rename_async', id=trans.security.encode_id(stored.id)),
                'annotate_async'      : h.url_for(controller='workflow', action='annotate_async', id=trans.security.encode_id(stored.id)),
                'get_new_module_info' : h.url_for(controller='workflow', action='get_new_module_info'),
                'workflow_index'      : h.url_for('/workflows/list'),
                'save_workflow'       : h.url_for(controller='workflow', action='save_workflow'),
                'workflow_save_as'    : h.url_for(controller='workflow', action='save_workflow_as')
            },
            'workflows' : [{
                'id'                  : trans.security.encode_id(workflow.id),
                'latest_id'           : trans.security.encode_id(workflow.latest_workflow.id),
                'step_count'          : len(workflow.latest_workflow.steps),
                'name'                : h.to_unicode(workflow.name)
            } for workflow in workflows]
        }
        
        
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_right_panel(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x1385f3a10')._populate(_import_ns, [u'render_individual_tagging_element'])
        h = _import_ns.get('h', context.get('h', UNDEFINED))
        trans = _import_ns.get('trans', context.get('trans', UNDEFINED))
        stored = _import_ns.get('stored', context.get('stored', UNDEFINED))
        annotation = _import_ns.get('annotation', context.get('annotation', UNDEFINED))
        render_individual_tagging_element = _import_ns.get('render_individual_tagging_element', context.get('render_individual_tagging_element', UNDEFINED))
        __M_writer = context.writer()
        __M_writer(u'\n    <div class="unified-panel-header" unselectable="on">\n        <div class="unified-panel-header-inner">\n            Details\n        </div>\n    </div>\n    <div class="unified-panel-body workflow-right" style="overflow: auto;">\n')
        __M_writer(u'        <div id="edit-attributes" class="metadataForm right-content">\n            <div class="metadataFormTitle">Edit Workflow Attributes</div>\n            <div class="metadataFormBody">\n')
        __M_writer(u'            <div id="workflow-name-area" class="form-row">\n                <label>Name:</label>\n                <span id="workflow-name" class="editable-text" title="Click to rename workflow">')
        __M_writer(filters.html_escape(unicode(h.to_unicode( stored.name ) )))
        __M_writer(u'</span>\n            </div>\n            <div id="workflow-version-area" class="form-row">\n                <label>Version:</label>\n            </div>\n            <select id="workflow-version-switch" href="#">Select version</select>\n')
        __M_writer(u'            ')
        __M_writer(u'\n            <div class="form-row">\n                <label>\n                    Tags:\n                </label>\n                    <div style="float: left; width: 225px; margin-right: 10px; border-style: inset; border-width: 1px; margin-left: 2px">\n                        <style>\n                            .tag-area {\n                                border: none;\n                            }\n                        </style>\n                        ')
        __M_writer(unicode(render_individual_tagging_element(user=trans.get_user(), tagged_item=stored, elt_context="edit_attributes.mako", use_toggle_link=False, input_size="20")))
        __M_writer(u'\n                    </div>\n                    <div class="toolParamHelp">Apply tags to make it easy to search for and find items with the same tag.</div>\n                </div>\n')
        __M_writer(u'                <div id="workflow-annotation-area" class="form-row">\n                    <label>Annotation / Notes:</label>\n                    <div id="workflow-annotation" class="editable-text" title="Click to edit annotation">\n')
        if annotation:
            __M_writer(u'                        ')
            __M_writer(filters.html_escape(unicode(h.to_unicode( annotation ) )))
            __M_writer(u'\n')
        else:
            __M_writer(u'                        <em>Describe or add notes to workflow</em>\n')
        __M_writer(u'                    </div>\n                    <div class="toolParamHelp">Add an annotation or notes to a workflow; annotations are available when a workflow is viewed.</div>\n                </div>\n            </div>\n        </div>\n\n')
        __M_writer(u'        <div id="right-content" class="right-content"></div>\n\n')
        __M_writer(u'        <div style="display:none;" id="workflow-output-area" class="metadataForm right-content">\n            <div class="metadataFormTitle">Edit Workflow Outputs</div>\n            <div class="metadataFormBody"><div class="form-row">\n                <div class="toolParamHelp">Tag step outputs to indicate the final dataset(s) to be generated by running this workflow.</div>\n                <div id="output-fill-area"></div>\n            </div></div>\n        </div>\n\n    </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_javascripts(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x1385f3a10')._populate(_import_ns, [u'render_individual_tagging_element'])
        h = _import_ns.get('h', context.get('h', UNDEFINED))
        self = _import_ns.get('self', context.get('self', UNDEFINED))
        parent = _import_ns.get('parent', context.get('parent', UNDEFINED))
        __M_writer = context.writer()
        __M_writer(u'\n\n    ')
        __M_writer(unicode(parent.javascripts()))
        __M_writer(u"\n\n    <script type='text/javascript'>\n        $( function() {\n            window.bundleEntries.workflow(")
        __M_writer(unicode(h.dumps(self.editor_config)))
        __M_writer(u');\n        });\n    </script>\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_render_tool(context,tool,section):
    __M_caller = context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x1385f3a10')._populate(_import_ns, [u'render_individual_tagging_element'])
        __M_writer = context.writer()
        __M_writer(u'\n    ')

        import markupsafe
            
        
        __M_writer(u'\n')
        if not tool.hidden:
            if tool.is_workflow_compatible:
                if section:
                    __M_writer(u'                <div class="toolTitle">\n')
                else:
                    __M_writer(u'                <div class="toolTitleNoSection">\n')
                if "[[" in tool.description and "]]" in tool.description:
                    __M_writer(u'                    ')
                    __M_writer(unicode(tool.description.replace( '[[', '<a id="link-${tool.id}" href="workflow_globals.app.add_node_for_tool( ${tool.id} )">' % tool.id ).replace( "]]", "</a>" )))
                    __M_writer(u'\n')
                elif tool.name:
                    __M_writer(u'                    <a id="link-')
                    __M_writer(unicode(tool.id))
                    __M_writer(u'" href="#" onclick="workflow_globals.app.add_node_for_tool( \'')
                    __M_writer(unicode(tool.id))
                    __M_writer(u"', '")
                    __M_writer(filters.html_escape(unicode(markupsafe.escape( tool.name ) )))
                    __M_writer(u'\' )" style="text-decoration: none; display: block;"><span style="text-decoration: underline">')
                    __M_writer(filters.html_escape(unicode(tool.name )))
                    __M_writer(u'</span> ')
                    __M_writer(unicode(tool.description))
                    __M_writer(u'</a>\n')
                else:
                    __M_writer(u'                    <a id="link-')
                    __M_writer(unicode(tool.id))
                    __M_writer(u'" href="#" onclick="workflow_globals.app.add_node_for_tool( \'')
                    __M_writer(unicode(tool.id))
                    __M_writer(u"', '")
                    __M_writer(filters.html_escape(unicode(markupsafe.escape( tool.name ) )))
                    __M_writer(u'\' )">')
                    __M_writer(unicode(tool.description))
                    __M_writer(u'</a>\n')
                __M_writer(u'            </div>\n')
            else:
                if section:
                    __M_writer(u'                <div class="toolTitleDisabled">\n')
                else:
                    __M_writer(u'                <div class="toolTitleNoSectionDisabled">\n')
                if "[[" in tool.description and "]]" in tool.description:
                    __M_writer(u'                    ')
                    __M_writer(unicode(tool.description.replace( '[[', '' % tool.id ).replace( "]]", "" )))
                    __M_writer(u'\n')
                elif tool.name:
                    __M_writer(u'                    ')
                    __M_writer(unicode(tool.name))
                    __M_writer(u' ')
                    __M_writer(unicode(tool.description))
                    __M_writer(u'\n')
                else:
                    __M_writer(u'                    ')
                    __M_writer(unicode(tool.description))
                    __M_writer(u'\n')
                __M_writer(u'            </div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "ascii", "line_map": {"23": 276, "29": 0, "36": 1, "37": 6, "38": 34, "39": 46, "40": 60, "41": 98, "42": 105, "43": 110, "44": 128, "45": 220, "46": 253, "47": 320, "53": 130, "69": 130, "70": 131, "75": 134, "76": 138, "77": 138, "78": 153, "83": 156, "84": 158, "85": 158, "86": 162, "87": 163, "88": 164, "89": 165, "90": 165, "91": 165, "92": 166, "93": 167, "94": 167, "96": 167, "97": 168, "98": 168, "99": 169, "100": 169, "101": 171, "102": 171, "103": 173, "104": 174, "105": 175, "106": 175, "107": 175, "108": 176, "109": 177, "110": 177, "111": 177, "112": 180, "113": 182, "114": 183, "115": 183, "116": 183, "117": 185, "118": 188, "119": 189, "120": 196, "121": 197, "122": 197, "123": 197, "124": 199, "125": 204, "126": 206, "127": 207, "128": 208, "129": 208, "130": 208, "131": 211, "132": 213, "138": 3, "144": 3, "150": 101, "156": 101, "157": 102, "158": 102, "159": 103, "160": 103, "166": 222, "174": 222, "175": 229, "176": 229, "182": 107, "190": 107, "191": 108, "193": 109, "199": 113, "205": 113, "206": 114, "207": 114, "208": 115, "209": 115, "210": 117, "211": 117, "212": 119, "213": 120, "214": 121, "215": 121, "216": 121, "217": 121, "218": 121, "219": 121, "220": 121, "221": 121, "222": 122, "223": 122, "224": 126, "230": 48, "238": 48, "239": 51, "240": 51, "241": 51, "242": 54, "243": 54, "244": 54, "250": 8, "262": 8, "263": 9, "289": 33, "295": 255, "306": 255, "307": 263, "308": 267, "309": 269, "310": 269, "311": 276, "312": 276, "313": 287, "314": 287, "315": 293, "316": 296, "317": 297, "318": 297, "319": 297, "320": 298, "321": 299, "322": 301, "323": 308, "324": 311, "330": 36, "339": 36, "340": 38, "341": 38, "342": 42, "343": 42, "349": 63, "355": 63, "356": 64, "360": 66, "361": 67, "362": 68, "363": 69, "364": 70, "365": 71, "366": 72, "367": 74, "368": 75, "369": 75, "370": 75, "371": 76, "372": 77, "373": 77, "374": 77, "375": 77, "376": 77, "377": 77, "378": 77, "379": 77, "380": 77, "381": 77, "382": 77, "383": 78, "384": 79, "385": 79, "386": 79, "387": 79, "388": 79, "389": 79, "390": 79, "391": 79, "392": 79, "393": 81, "394": 82, "395": 83, "396": 84, "397": 85, "398": 86, "399": 88, "400": 89, "401": 89, "402": 89, "403": 90, "404": 91, "405": 91, "406": 91, "407": 91, "408": 91, "409": 92, "410": 93, "411": 93, "412": 93, "413": 95, "419": 413}, "uri": "workflow/editor.mako", "filename": "templates/webapps/galaxy/workflow/editor.mako"}
__M_END_METADATA
"""
