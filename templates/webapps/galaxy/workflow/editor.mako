<%inherit file="/webapps/galaxy/base_panels.mako"/>

<%def name="title()">

    Workflow Editor
</%def>

<%def name="init()">
<%
    self.active_view="workflow"
    self.overlay_visible=True
%>
</%def>

<<<<<<< HEAD
<%def name="javascripts()">

    ${parent.javascripts()}

    <script type='text/javascript'>
        $( function() {
            window.bundleEntries.workflow(${h.dumps(self.editor_config)});
=======
<%def name="javascript_app()">
    ${parent.javascript_app()}
    <script type="text/javascript">
        var editorConfig = ${ h.dumps( editor_config ) };
        config.addInitialization(function(galaxy, config) {
            console.log("workflow/editor.mako, editorConfig", editorConfig);
            window.bundleEntries.mountWorkflowEditor(editorConfig);
>>>>>>> refs/heads/release_21.01
        });
    </script>
</%def>

<%def name="stylesheets()">
    ## Include "base.css" for styling tool menu and forms (details)
    ${h.css( "base", "autocomplete_tagging", "jquery-ui/smoothness/jquery-ui" )}

    ## But make sure styles for the layout take precedence
    ${parent.stylesheets()}
<<<<<<< HEAD

    <style type="text/css">
    canvas { position: absolute; z-index: 10; }
    canvas.dragging { position: absolute; z-index: 1000; }
    </style>
</%def>

## Render a tool in the tool panel
<%def name="render_tool( tool, section )">
    <%
        import markupsafe
    %>
    %if not tool.hidden:
        %if tool.is_workflow_compatible:
            %if section:
                <div class="toolTitle">
            %else:
                <div class="toolTitleNoSection">
            %endif
                %if "[[" in tool.description and "]]" in tool.description:
                    ${tool.description.replace( '[[', '<a id="link-${tool.id}" href="workflow_globals.app.add_node_for_tool( ${tool.id} )">' % tool.id ).replace( "]]", "</a>" )}
                %elif tool.name:
                    <a id="link-${tool.id}" href="#" onclick="workflow_globals.app.add_node_for_tool( '${tool.id}', '${markupsafe.escape( tool.name ) | h}' )" style="text-decoration: none; display: block;"><span style="text-decoration: underline">${tool.name | h}</span> ${tool.description}</a>
                %else:
                    <a id="link-${tool.id}" href="#" onclick="workflow_globals.app.add_node_for_tool( '${tool.id}', '${markupsafe.escape( tool.name ) | h}' )">${tool.description}</a>
                %endif
            </div>
        %else:
            %if section:
                <div class="toolTitleDisabled">
            %else:
                <div class="toolTitleNoSectionDisabled">
            %endif
                %if "[[" in tool.description and "]]" in tool.description:
                    ${tool.description.replace( '[[', '' % tool.id ).replace( "]]", "" )}
                %elif tool.name:
                    ${tool.name} ${tool.description}
                %else:
                    ${tool.description}
                %endif
            </div>
        %endif
    %endif
</%def>

## Render a label in the tool panel
<%def name="render_label( label )">
    <div class="toolPanelLabel" id="title_${label.id}">
        <span>${label.text}</span>
    </div>
=======
>>>>>>> refs/heads/release_21.01
</%def>

<%def name="overlay(visible=False)">
    ${parent.overlay( "Loading workflow...",
                      "<div class='progress progress-striped progress-info active'><div class='progress-bar' style='width: 100%;'></div></div>", self.overlay_visible )}
</%def>

<%def name="left_panel()">
</%def>

<%def name="center_panel()">
<<<<<<< HEAD

    <div class="unified-panel-header" unselectable="on">
        <div class="panel-header-buttons">
            <a id="workflow-options-button" class="panel-header-button" href="#"><span class="fa fa-cog"></span></a>
        </div>
        <div class="unified-panel-header-inner">
            ${h.to_unicode( stored.name ) | h}
        </div>
    </div>
    <div class="unified-panel-body" id="workflow-canvas-body">
        <div id="canvas-viewport">
            <div id="canvas-container" style="position: absolute; width: 100%; height: 100%;"></div>
        </div>
        <div id='workflow-parameters-box' style="display:none; position: absolute; right:0px; border: solid grey 1px; padding: 5px; background: #EEEEEE; z-index: 20000; overflow: auto; max-width: 300px; max-height: 300px;">
            <div style="margin-bottom:5px;">
                <b>Workflow Parameters</b>
            </div>
            <div id="workflow-parameters-container">
            </div>
        </div>
        <div class="workflow-overview">
            <div style="position: relative; overflow: hidden; width: 100%; height: 100%; border-top: solid gray 1px; border-left: solid grey 1px;">
                <div id="overview" style="position: absolute;">
                    <canvas width="0" height="0" style="background: white; width: 100%; height: 100%;" id="overview-canvas"></canvas>
                    <div id="overview-viewport" style="position: absolute; width: 0px; height: 0px; border: solid blue 1px; z-index: 10;"></div>
                </div>
            </div>
        </div>
    </div>

=======
>>>>>>> refs/heads/release_21.01
</%def>

<%def name="right_panel()">
<<<<<<< HEAD
    <div class="unified-panel-header" unselectable="on">
        <div class="unified-panel-header-inner">
            Details
        </div>
    </div>
    <div class="unified-panel-body workflow-right" style="overflow: auto;">
        ## Div for elements to modify workflow attributes.
        <div id="edit-attributes" class="metadataForm right-content">
            <div class="metadataFormTitle">Edit Workflow Attributes</div>
            <div class="metadataFormBody">
            ## Workflow name.
            <div id="workflow-name-area" class="form-row">
                <label>Name:</label>
                <span id="workflow-name" class="editable-text" title="Click to rename workflow">${h.to_unicode( stored.name ) | h}</span>
            </div>
            <div id="workflow-version-area" class="form-row">
                <label>Version:</label>
            </div>
            <select id="workflow-version-switch" href="#">Select version</select>
            ## Workflow tags.
            <%namespace file="/tagging_common.mako" import="render_individual_tagging_element" />
            <div class="form-row">
                <label>
                    Tags:
                </label>
                    <div style="float: left; width: 225px; margin-right: 10px; border-style: inset; border-width: 1px; margin-left: 2px">
                        <style>
                            .tag-area {
                                border: none;
                            }
                        </style>
                        ${render_individual_tagging_element(user=trans.get_user(), tagged_item=stored, elt_context="edit_attributes.mako", use_toggle_link=False, input_size="20")}
                    </div>
                    <div class="toolParamHelp">Apply tags to make it easy to search for and find items with the same tag.</div>
                </div>
                ## Workflow annotation.
                ## Annotation elt.
                <div id="workflow-annotation-area" class="form-row">
                    <label>Annotation / Notes:</label>
                    <div id="workflow-annotation" class="editable-text" title="Click to edit annotation">
                    %if annotation:
                        ${h.to_unicode( annotation ) | h}
                    %else:
                        <em>Describe or add notes to workflow</em>
                    %endif
                    </div>
                    <div class="toolParamHelp">Add an annotation or notes to a workflow; annotations are available when a workflow is viewed.</div>
                </div>
            </div>
        </div>

        ## Div where tool details are loaded and modified.
        <div id="right-content" class="right-content"></div>

        ## Workflow output tagging
        <div style="display:none;" id="workflow-output-area" class="metadataForm right-content">
            <div class="metadataFormTitle">Edit Workflow Outputs</div>
            <div class="metadataFormBody"><div class="form-row">
                <div class="toolParamHelp">Tag step outputs to indicate the final dataset(s) to be generated by running this workflow.</div>
                <div id="output-fill-area"></div>
            </div></div>
        </div>

    </div>
=======
>>>>>>> refs/heads/release_21.01
</%def>
