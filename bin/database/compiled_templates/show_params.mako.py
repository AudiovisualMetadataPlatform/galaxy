# -*- coding:ascii -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
STOP_RENDERING = runtime.STOP_RENDERING
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 10
_modified_time = 1568313263.660611
_enable_loop = True
_template_filename = 'templates/show_params.mako'
_template_uri = 'show_params.mako'
_source_encoding = 'ascii'
_exports = ['inputs_recursive_indent', 'inputs_recursive']


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    ns = runtime.TemplateNamespace('__anon_0x118171950', context._clean_inheritance_tokens(), templateuri=u'/message.mako', callables=None,  calling_uri=_template_uri)
    context.namespaces[(__name__, '__anon_0x118171950')] = ns

def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'/base.mako', _template_uri)
def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x118171950')._populate(_import_ns, [u'render_msg'])
        upgrade_messages = _import_ns.get('upgrade_messages', context.get('upgrade_messages', UNDEFINED))
        render_msg = _import_ns.get('render_msg', context.get('render_msg', UNDEFINED))
        str = _import_ns.get('str', context.get('str', UNDEFINED))
        h = _import_ns.get('h', context.get('h', UNDEFINED))
        inherit_chain = _import_ns.get('inherit_chain', context.get('inherit_chain', UNDEFINED))
        tool = _import_ns.get('tool', context.get('tool', UNDEFINED))
        def inputs_recursive(input_params,param_values,depth=1,upgrade_messages=None):
            return render_inputs_recursive(context._locals(__M_locals),input_params,param_values,depth,upgrade_messages)
        filter = _import_ns.get('filter', context.get('filter', UNDEFINED))
        job = _import_ns.get('job', context.get('job', UNDEFINED))
        set = _import_ns.get('set', context.get('set', UNDEFINED))
        hda = _import_ns.get('hda', context.get('hda', UNDEFINED))
        sorted = _import_ns.get('sorted', context.get('sorted', UNDEFINED))
        trans = _import_ns.get('trans', context.get('trans', UNDEFINED))
        params_objects = _import_ns.get('params_objects', context.get('params_objects', UNDEFINED))
        has_parameter_errors = _import_ns.get('has_parameter_errors', context.get('has_parameter_errors', UNDEFINED))
        __M_writer = context.writer()
        __M_writer(u'\n')
        __M_writer(u'\n')
        from galaxy.util import nice_size, unicodify 
        
        __M_locals_builtin_stored = __M_locals_builtin()
        __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['nice_size','unicodify'] if __M_key in __M_locals_builtin_stored]))
        __M_writer(u'\n\n<style>\n    .inherit {\n        border: 1px solid #bbb;\n        padding: 15px;\n        text-align: center;\n        background-color: #eee;\n    }\n\n    table.info_data_table {\n        table-layout: fixed;\n        word-break: break-word;\n    }\n    table.info_data_table td:nth-child(1) {\n        width: 25%;\n    }\n\n</style>\n\n')
        __M_writer(u'\n\n')
        __M_writer(u'\n\n<h2>\n')
        if tool:
            __M_writer(u'    ')
            __M_writer(filters.html_escape(unicode(tool.name )))
            __M_writer(u'\n')
        else:
            __M_writer(u'    Unknown Tool\n')
        __M_writer(u'</h2>\n\n<h3>Dataset Information</h3>\n<table class="tabletip" id="dataset-details">\n    <tbody>\n        ')

        encoded_hda_id = trans.security.encode_id( hda.id )
        encoded_history_id = trans.security.encode_id( hda.history_id )
        
        
        __M_locals_builtin_stored = __M_locals_builtin()
        __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['encoded_hda_id','encoded_history_id'] if __M_key in __M_locals_builtin_stored]))
        __M_writer(u'\n        <tr><td>Number:</td><td>')
        __M_writer(filters.html_escape(unicode(hda.hid )))
        __M_writer(u'</td></tr>\n        <tr><td>Name:</td><td>')
        __M_writer(filters.html_escape(unicode(hda.name )))
        __M_writer(u'</td></tr>\n        <tr><td>Created:</td><td>')
        __M_writer(unicode(unicodify(hda.create_time.strftime(trans.app.config.pretty_datetime_format))))
        __M_writer(u'</td></tr>\n')
        __M_writer(u'        <tr><td>Filesize:</td><td>')
        __M_writer(unicode(nice_size(hda.dataset.file_size)))
        __M_writer(u'</td></tr>\n        <tr><td>Dbkey:</td><td>')
        __M_writer(filters.html_escape(unicode(hda.dbkey )))
        __M_writer(u'</td></tr>\n        <tr><td>Format:</td><td>')
        __M_writer(filters.html_escape(unicode(hda.ext )))
        __M_writer(u'</td></tr>\n    </tbody>\n</table>\n\n<h3>Job Information</h3>\n<table class="tabletip">\n    <tbody>\n')
        if job:
            __M_writer(u'            <tr><td>Galaxy Tool ID:</td><td>')
            __M_writer(filters.html_escape(unicode( job.tool_id )))
            __M_writer(u'</td></tr>\n            <tr><td>Galaxy Tool Version:</td><td>')
            __M_writer(filters.html_escape(unicode( job.tool_version )))
            __M_writer(u'</td></tr>\n')
        __M_writer(u'        <tr><td>Tool Version:</td><td>')
        __M_writer(filters.html_escape(unicode(hda.tool_version )))
        __M_writer(u'</td></tr>\n        <tr><td>Tool Standard Output:</td><td><a href="')
        __M_writer(unicode(h.url_for( controller='dataset', action='stdout', dataset_id=encoded_hda_id )))
        __M_writer(u'">stdout</a></td></tr>\n        <tr><td>Tool Standard Error:</td><td><a href="')
        __M_writer(unicode(h.url_for( controller='dataset', action='stderr', dataset_id=encoded_hda_id )))
        __M_writer(u'">stderr</a></td></tr>\n')
        if job:
            __M_writer(u'            <tr><td>Tool Exit Code:</td><td>')
            __M_writer(filters.html_escape(unicode( job.exit_code )))
            __M_writer(u'</td></tr>\n')
        __M_writer(u'        <tr><td>History Content API ID:</td>\n        <td>')
        __M_writer(unicode(encoded_hda_id))
        __M_writer(u'\n')
        if trans.user_is_admin:
            __M_writer(u'                (')
            __M_writer(unicode(hda.id))
            __M_writer(u')\n')
        __M_writer(u'        </td></tr>\n')
        if job:
            __M_writer(u'            <tr><td>Job API ID:</td>\n            <td>')
            __M_writer(unicode(trans.security.encode_id( job.id )))
            __M_writer(u'\n')
            if trans.user_is_admin:
                __M_writer(u'                    (')
                __M_writer(unicode(job.id))
                __M_writer(u')\n')
            __M_writer(u'            </td></tr>\n')
        __M_writer(u'        <tr><td>History API ID:</td>\n        <td>')
        __M_writer(unicode(encoded_history_id))
        __M_writer(u'\n')
        if trans.user_is_admin:
            __M_writer(u'                (')
            __M_writer(unicode(hda.history_id))
            __M_writer(u')\n')
        __M_writer(u'        </td></tr>\n')
        if hda.dataset.uuid:
            __M_writer(u'        <tr><td>UUID:</td><td>')
            __M_writer(unicode(hda.dataset.uuid))
            __M_writer(u'</td></tr>\n')
        if trans.user_is_admin or trans.app.config.expose_dataset_path:
            if not hda.purged:
                __M_writer(u'                <tr><td>Full Path:</td><td>')
                __M_writer(filters.html_escape(unicode(hda.file_name )))
                __M_writer(u'</td></tr>\n')
        __M_writer(u'    </tbody>\n</table>\n\n<h3>Tool Parameters</h3>\n<table class="tabletip" id="tool-parameters">\n    <thead>\n        <tr>\n            <th>Input Parameter</th>\n            <th>Value</th>\n            <th>Note for rerun</th>\n        </tr>\n    </thead>\n    <tbody>\n')
        if params_objects and tool:
            __M_writer(u'            ')
            __M_writer(unicode( inputs_recursive( tool.inputs, params_objects, depth=1, upgrade_messages=upgrade_messages ) ))
            __M_writer(u'\n')
        elif params_objects is None:
            __M_writer(u'            <tr><td colspan="3">Unable to load parameters.</td></tr>\n')
        else:
            __M_writer(u'            <tr><td colspan="3">No parameters.</td></tr>\n')
        __M_writer(u'    </tbody>\n</table>\n')
        if has_parameter_errors:
            __M_writer(u'    <br />\n    ')
            __M_writer(unicode( render_msg( 'One or more of your original parameters may no longer be valid or displayed properly.', status='warning' ) ))
            __M_writer(u'\n')
        __M_writer(u'\n\n<h3>Inheritance Chain</h3>\n<div class="inherit" style="background-color: #fff; font-weight:bold;">')
        __M_writer(filters.html_escape(unicode(hda.name )))
        __M_writer(u'</div>\n\n')
        for dep in inherit_chain:
            __M_writer(u'    <div style="font-size: 36px; text-align: center; position: relative; top: 3px">&uarr;</div>\n    <div class="inherit">\n        \'')
            __M_writer(filters.html_escape(unicode(dep[0].name )))
            __M_writer(u"' in ")
            __M_writer(unicode(dep[1]))
            __M_writer(u'<br/>\n    </div>\n')
        __M_writer(u'\n\n\n')
        if job and job.command_line and (trans.user_is_admin or trans.app.config.expose_dataset_path):
            __M_writer(u'<h3>Command Line</h3>\n<pre class="code">\n')
            __M_writer(filters.html_escape(unicode( job.command_line )))
            __M_writer(u'</pre>\n')
        __M_writer(u'\n')
        if job and (trans.user_is_admin or trans.app.config.expose_potentially_sensitive_job_metrics):
            __M_writer(u'<h3>Job Metrics</h3>\n')
            job_metrics = trans.app.job_metrics 
            
            __M_locals_builtin_stored = __M_locals_builtin()
            __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['job_metrics'] if __M_key in __M_locals_builtin_stored]))
            __M_writer(u'\n')
            plugins = set([metric.plugin for metric in job.metrics]) 
            
            __M_locals_builtin_stored = __M_locals_builtin()
            __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['metric','plugins'] if __M_key in __M_locals_builtin_stored]))
            __M_writer(u'\n')
            for plugin in sorted(plugins):
                if trans.user_is_admin or plugin != 'env':
                    __M_writer(u'    <h4>')
                    __M_writer(filters.html_escape(unicode( plugin )))
                    __M_writer(u'</h4>\n    <table class="tabletip info_data_table">\n        <tbody>\n        ')

                    plugin_metrics = filter(lambda x: x.plugin == plugin, job.metrics)
                    plugin_metric_displays = [job_metrics.format( metric.plugin, metric.metric_name, metric.metric_value ) for metric in plugin_metrics]
                    plugin_metric_displays = sorted(plugin_metric_displays, key=lambda pair: pair[0])  # Sort on displayed title
                            
                    
                    __M_locals_builtin_stored = __M_locals_builtin()
                    __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['plugin_metric_displays','metric','plugin_metrics'] if __M_key in __M_locals_builtin_stored]))
                    __M_writer(u'\n')
                    for metric_title, metric_value in plugin_metric_displays:
                        __M_writer(u'                <tr><td>')
                        __M_writer(filters.html_escape(unicode( metric_title )))
                        __M_writer(u'</td><td>')
                        __M_writer(filters.html_escape(unicode( metric_value )))
                        __M_writer(u'</td></tr>\n')
                    __M_writer(u'        </tbody>\n    </table>\n')
        __M_writer(u'\n')
        if trans.user_is_admin:
            __M_writer(u'<h3>Destination Parameters</h3>\n    <table class="tabletip">\n        <tbody>\n            <tr><th scope="row">Runner</th><td>')
            __M_writer(unicode( job.job_runner_name ))
            __M_writer(u'</td></tr>\n            <tr><th scope="row">Runner Job ID</th><td>')
            __M_writer(unicode( job.job_runner_external_id ))
            __M_writer(u'</td></tr>\n            <tr><th scope="row">Handler</th><td>')
            __M_writer(unicode( job.handler ))
            __M_writer(u'</td></tr>\n')
            if job.destination_params:
                for (k, v) in job.destination_params.items():
                    __M_writer(u'                <tr><th scope="row">')
                    __M_writer(filters.html_escape(unicode( k )))
                    __M_writer(u'</th>\n                    <td>\n')
                    if str(k) in ('nativeSpecification', 'rank', 'requirements'):
                        __M_writer(u'                        <pre style="white-space: pre-wrap; word-wrap: break-word;">')
                        __M_writer(filters.html_escape(unicode( v )))
                        __M_writer(u'</pre>\n')
                    else:
                        __M_writer(u'                        ')
                        __M_writer(filters.html_escape(unicode( v )))
                        __M_writer(u'\n')
                    __M_writer(u'                    </td>\n                </tr>\n')
            __M_writer(u'        </tbody>\n    </table>\n')
        __M_writer(u'\n')
        if job and job.dependencies:
            __M_writer(u'<h3>Job Dependencies</h3>\n    <table class="tabletip">\n        <thead>\n        <tr>\n            <th>Dependency</th>\n            <th>Dependency Type</th>\n            <th>Version</th>\n')
            if trans.user_is_admin:
                __M_writer(u'            <th>Path</th>\n')
            __M_writer(u'        </tr>\n        </thead>\n        <tbody>\n\n')
            for dependency in job.dependencies:
                __M_writer(u'                <tr><td>')
                __M_writer(filters.html_escape(unicode( dependency['name'] )))
                __M_writer(u'</td>\n                    <td>')
                __M_writer(filters.html_escape(unicode( dependency['dependency_type'] )))
                __M_writer(u'</td>\n                    <td>')
                __M_writer(filters.html_escape(unicode( dependency['version'] )))
                __M_writer(u'</td>\n')
                if trans.user_is_admin:
                    if 'environment_path' in dependency:
                        __M_writer(u'                        <td>')
                        __M_writer(filters.html_escape(unicode( dependency['environment_path'] )))
                        __M_writer(u'</td>\n')
                    elif 'path' in dependency:
                        __M_writer(u'                        <td>')
                        __M_writer(filters.html_escape(unicode( dependency['path'] )))
                        __M_writer(u'</td>\n')
                    else:
                        __M_writer(u'                        <td></td>\n')
                __M_writer(u'                </tr>\n')
            __M_writer(u'\n        </tbody>\n    </table>\n')
        __M_writer(u'\n')
        if hda.peek:
            __M_writer(u'    <h3>Dataset peek</h3>\n    <pre class="dataset-peek">')
            __M_writer(unicode(hda.peek))
            __M_writer(u'\n    </pre>\n')
        __M_writer(u'\n\n<script type="text/javascript">\n$(function(){\n    $( \'.input-dataset-show-params\' ).on( \'click\', function( ev ){\n')
        __M_writer(u"        if( window.parent.Galaxy && window.parent.Galaxy.currHistoryPanel ){\n            window.parent.Galaxy.currHistoryPanel.scrollToId( 'dataset-' + $( this ).data( 'hda-id' ) );\n        }\n    })\n});\n</script>\n")
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_inputs_recursive_indent(context,text,depth):
    __M_caller = context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x118171950')._populate(_import_ns, [u'render_msg'])
        __M_writer = context.writer()
        __M_writer(u'\n    <td style="padding-left: ')
        __M_writer(unicode( ( depth - 1 ) * 10 ))
        __M_writer(u'px">\n        ')
        __M_writer(filters.html_escape(unicode(text )))
        __M_writer(u'\n    </td>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_inputs_recursive(context,input_params,param_values,depth=1,upgrade_messages=None):
    __M_caller = context.caller_stack._push_frame()
    try:
        _import_ns = {}
        _mako_get_namespace(context, '__anon_0x118171950')._populate(_import_ns, [u'render_msg'])
        h = _import_ns.get('h', context.get('h', UNDEFINED))
        len = _import_ns.get('len', context.get('len', UNDEFINED))
        def inputs_recursive_indent(text,depth):
            return render_inputs_recursive_indent(context,text,depth)
        range = _import_ns.get('range', context.get('range', UNDEFINED))
        def inputs_recursive(input_params,param_values,depth=1,upgrade_messages=None):
            return render_inputs_recursive(context,input_params,param_values,depth,upgrade_messages)
        enumerate = _import_ns.get('enumerate', context.get('enumerate', UNDEFINED))
        trans = _import_ns.get('trans', context.get('trans', UNDEFINED))
        hasattr = _import_ns.get('hasattr', context.get('hasattr', UNDEFINED))
        __M_writer = context.writer()
        __M_writer(u'\n    ')

        from galaxy.util import listify
        if upgrade_messages is None:
            upgrade_messages = {}
            
        
        __M_writer(u'\n')
        for input_index, input in enumerate( input_params.values() ):
            if input.name in param_values:
                if input.type == "repeat":
                    for i in range( len(param_values[input.name]) ):
                        __M_writer(u'                    ')
                        __M_writer(unicode( inputs_recursive(input.inputs, param_values[input.name][i], depth=depth+1) ))
                        __M_writer(u'\n')
                elif input.type == "section":
                    __M_writer(u'                <tr>\n')
                    __M_writer(u'                    ')
                    __M_writer(unicode(inputs_recursive_indent( text=input.name, depth=depth )))
                    __M_writer(u'\n                    <td></td>\n                </tr>\n                ')
                    __M_writer(unicode( inputs_recursive( input.inputs, param_values[input.name], depth=depth+1, upgrade_messages=upgrade_messages.get( input.name ) ) ))
                    __M_writer(u'\n')
                elif input.type == "conditional":
                    __M_writer(u'                ')

                    try:
                        current_case = param_values[input.name]['__current_case__']
                        is_valid = True
                    except:
                        current_case = None
                        is_valid = False
                    
                    
                    __M_writer(u'\n')
                    if is_valid:
                        __M_writer(u'                    <tr>\n                        ')
                        __M_writer(unicode( inputs_recursive_indent( text=input.test_param.label, depth=depth )))
                        __M_writer(u'\n')
                        __M_writer(u'                        <td>')
                        __M_writer(filters.html_escape(unicode(input.cases[current_case].value )))
                        __M_writer(u'</td>\n                        <td></td>\n                    </tr>\n                    ')
                        __M_writer(unicode( inputs_recursive( input.cases[current_case].inputs, param_values[input.name], depth=depth+1, upgrade_messages=upgrade_messages.get( input.name ) ) ))
                        __M_writer(u'\n')
                    else:
                        __M_writer(u'                    <tr>\n                        ')
                        __M_writer(unicode( inputs_recursive_indent( text=input.name, depth=depth )))
                        __M_writer(u'\n                        <td><em>The previously used value is no longer valid</em></td>\n                        <td></td>\n                    </tr>\n')
                elif input.type == "upload_dataset":
                    __M_writer(u'                    <tr>\n                        ')
                    __M_writer(unicode(inputs_recursive_indent( text=input.group_title( param_values ), depth=depth )))
                    __M_writer(u'\n                        <td>')
                    __M_writer(unicode( len( param_values[input.name] ) ))
                    __M_writer(u' uploaded datasets</td>\n                        <td></td>\n                    </tr>\n')
                elif input.type == "data":
                    __M_writer(u'                    <tr>\n                        ')
                    __M_writer(unicode(inputs_recursive_indent( text=input.label, depth=depth )))
                    __M_writer(u'\n                        <td>\n')
                    for i, element in enumerate(listify(param_values[input.name])):
                        if i > 0:
                            __M_writer(u'                            ,\n')
                        if element.history_content_type == "dataset":
                            __M_writer(u'                                ')

                            hda = element
                            encoded_id = trans.security.encode_id( hda.id )
                            show_params_url = h.url_for( controller='dataset', action='show_params', dataset_id=encoded_id )
                                                            
                            
                            __M_writer(u'\n                                <a class="input-dataset-show-params" data-hda-id="')
                            __M_writer(unicode(encoded_id))
                            __M_writer(u'"\n                                       href="')
                            __M_writer(unicode(show_params_url))
                            __M_writer(u'">')
                            __M_writer(unicode(hda.hid))
                            __M_writer(u': ')
                            __M_writer(filters.html_escape(unicode(hda.name )))
                            __M_writer(u'</a>\n\n')
                        else:
                            __M_writer(u'                                ')
                            __M_writer(unicode(element.hid))
                            __M_writer(u': ')
                            __M_writer(filters.html_escape(unicode(element.name )))
                            __M_writer(u'\n')
                    __M_writer(u'                        </td>\n                        <td></td>\n                    </tr>\n')
                elif input.visible:
                    __M_writer(u'                ')

                    if  hasattr( input, "label" ) and input.label:
                        label = input.label
                    else:
                        #value for label not required, fallback to input name (same as tool panel)
                        label = input.name
                    
                    
                    __M_writer(u'\n                <tr>\n                    ')
                    __M_writer(unicode(inputs_recursive_indent( text=label, depth=depth )))
                    __M_writer(u'\n                    <td>')
                    __M_writer(filters.html_escape(unicode(input.value_to_display_text( param_values[input.name] ) )))
                    __M_writer(u'</td>\n                    <td>')
                    __M_writer(filters.html_escape(unicode( upgrade_messages.get( input.name, '' ) )))
                    __M_writer(u'</td>\n                </tr>\n')
            else:
                __M_writer(u'            <tr>\n                ')

                    # Get parameter label.
                if input.type == "conditional":
                    label = input.test_param.label
                elif input.type == "repeat":
                    label = input.label()
                else:
                    label = input.label or input.name
                                
                
                __M_writer(u'\n                ')
                __M_writer(unicode(inputs_recursive_indent( text=label, depth=depth )))
                __M_writer(u'\n                <td><em>not used (parameter was added after this job was run)</em></td>\n                <td></td>\n            </tr>\n')
            __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


"""
__M_BEGIN_METADATA
{"source_encoding": "ascii", "line_map": {"23": 2, "29": 0, "52": 1, "53": 2, "54": 3, "58": 3, "59": 130, "60": 137, "61": 140, "62": 141, "63": 141, "64": 141, "65": 142, "66": 143, "67": 145, "68": 150, "75": 153, "76": 154, "77": 154, "78": 155, "79": 155, "80": 156, "81": 156, "82": 158, "83": 158, "84": 158, "85": 159, "86": 159, "87": 160, "88": 160, "89": 167, "90": 168, "91": 168, "92": 168, "93": 169, "94": 169, "95": 171, "96": 171, "97": 171, "98": 172, "99": 172, "100": 173, "101": 173, "102": 174, "103": 175, "104": 175, "105": 175, "106": 177, "107": 178, "108": 178, "109": 179, "110": 180, "111": 180, "112": 180, "113": 182, "114": 183, "115": 184, "116": 185, "117": 185, "118": 186, "119": 187, "120": 187, "121": 187, "122": 189, "123": 191, "124": 192, "125": 192, "126": 193, "127": 194, "128": 194, "129": 194, "130": 196, "131": 197, "132": 198, "133": 198, "134": 198, "135": 200, "136": 201, "137": 202, "138": 202, "139": 202, "140": 205, "141": 218, "142": 219, "143": 219, "144": 219, "145": 220, "146": 221, "147": 222, "148": 223, "149": 225, "150": 227, "151": 228, "152": 229, "153": 229, "154": 231, "155": 234, "156": 234, "157": 236, "158": 237, "159": 239, "160": 239, "161": 239, "162": 239, "163": 242, "164": 245, "165": 246, "166": 248, "167": 248, "168": 250, "169": 251, "170": 252, "171": 253, "175": 253, "176": 254, "180": 254, "181": 255, "182": 256, "183": 257, "184": 257, "185": 257, "186": 260, "194": 264, "195": 265, "196": 266, "197": 266, "198": 266, "199": 266, "200": 266, "201": 268, "202": 273, "203": 274, "204": 275, "205": 278, "206": 278, "207": 279, "208": 279, "209": 280, "210": 280, "211": 281, "212": 282, "213": 283, "214": 283, "215": 283, "216": 285, "217": 286, "218": 286, "219": 286, "220": 287, "221": 288, "222": 288, "223": 288, "224": 290, "225": 294, "226": 297, "227": 298, "228": 299, "229": 306, "230": 307, "231": 309, "232": 313, "233": 314, "234": 314, "235": 314, "236": 315, "237": 315, "238": 316, "239": 316, "240": 317, "241": 318, "242": 319, "243": 319, "244": 319, "245": 320, "246": 321, "247": 321, "248": 321, "249": 322, "250": 323, "251": 326, "252": 328, "253": 332, "254": 333, "255": 334, "256": 335, "257": 335, "258": 338, "259": 344, "265": 133, "271": 133, "272": 134, "273": 134, "274": 135, "275": 135, "281": 23, "297": 23, "298": 24, "304": 28, "305": 29, "306": 30, "307": 31, "308": 32, "309": 33, "310": 33, "311": 33, "312": 35, "313": 36, "314": 38, "315": 38, "316": 38, "317": 41, "318": 41, "319": 42, "320": 43, "321": 43, "330": 50, "331": 51, "332": 52, "333": 53, "334": 53, "335": 55, "336": 55, "337": 55, "338": 58, "339": 58, "340": 59, "341": 60, "342": 61, "343": 61, "344": 66, "345": 67, "346": 68, "347": 68, "348": 69, "349": 69, "350": 73, "351": 74, "352": 75, "353": 75, "354": 77, "355": 78, "356": 79, "357": 81, "358": 82, "359": 82, "365": 86, "366": 87, "367": 87, "368": 88, "369": 88, "370": 88, "371": 88, "372": 88, "373": 88, "374": 90, "375": 91, "376": 91, "377": 91, "378": 91, "379": 91, "380": 94, "381": 97, "382": 98, "383": 98, "391": 104, "392": 106, "393": 106, "394": 107, "395": 107, "396": 108, "397": 108, "398": 111, "399": 113, "400": 114, "410": 122, "411": 123, "412": 123, "413": 128, "419": 413}, "uri": "show_params.mako", "filename": "templates/show_params.mako"}
__M_END_METADATA
"""
