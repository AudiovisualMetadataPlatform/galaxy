<%inherit file="/webapps/galaxy/base_panels.mako"/>

<%def name="title()">
    Page Editor
</%def>

<%def name="init()">
<%
    self.active_view="user"
%>
</%def>

<%def name="javascripts()">
    ${parent.javascripts()}
    <script type="text/javascript">
<<<<<<< HEAD
        // Define variables needed by galaxy.pages script.
        var page_id = "${trans.security.encode_id(page.id)}",
            page_list_url = '${h.url_for( controller='pages', action='list' )}',
            list_objects_url = "${h.url_for(controller='page', action='LIST_ACTION' )}",
            set_accessible_url = "${h.url_for( controller='ITEM_CONTROLLER', action='set_accessible_async' )}",
            get_name_and_link_url = "${h.url_for( controller='ITEM_CONTROLLER', action='get_name_and_link_async' )}?id=",
            editor_base_path = "${h.url_for('/static/wymeditor')}/",
            iframe_base_path = "${h.url_for('/static/wymeditor/iframe/galaxy')}/",
            save_url = "${h.url_for(controller='page', action='save' )}";

        $(function(){
            bundleEntries.pages()
=======
        config.addInitialization(function(){
            console.log("editor.mako, javascript_app", "define variables needed by galaxy.pages script");
            window.bundleEntries.mountPageEditor({
                pageId: "${id}",
            });
>>>>>>> refs/heads/release_21.01
        });

    </script>
</%def>

<<<<<<< HEAD
<%def name="stylesheets()">
    ${parent.stylesheets()}
    ${h.css( "base", "autocomplete_tagging", "embed_item" )}
    <style type='text/css'>
        .galaxy-page-editor-button
        {
            position: relative;
            float: left;
            padding: 0.2em;
        }
    </style>
=======
<%def name="left_panel()">
>>>>>>> refs/heads/release_21.01
</%def>

<%def name="center_panel()">
</%def>

<%def name="right_panel()">
</%def>

