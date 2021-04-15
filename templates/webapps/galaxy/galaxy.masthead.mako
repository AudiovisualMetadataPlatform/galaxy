<%namespace file="/galaxy_client_app.mako" import="get_user_dict" />

## masthead head generator
<%def name="load(active_view = None)">
    <%
        from markupsafe import escape
        ## get configuration
        masthead_config = {
            ## inject configuration
            'brand'                     : app.config.brand or '',
            'display_galaxy_brand'      : app.config.display_galaxy_brand,
            'nginx_upload_path'         : app.config.nginx_upload_path or h.url_for(controller='api', action='tools'),
            'use_remote_user'           : app.config.use_remote_user,
            'remote_user_logout_href'   : app.config.remote_user_logout_href,
            'enable_cloud_launch'       : app.config.get_bool('enable_cloud_launch', False),
            'lims_doc_url'              : app.config.get("lims_doc_url", "https://usegalaxy.org/u/rkchak/p/sts"),
<<<<<<< HEAD
            'biostar_url'               : app.config.biostar_url,
            'biostar_url_redirect'      : h.url_for( controller='biostar', action='biostar_redirect', qualified=True ),
            'default_locale'            : app.config.get("default_locale",  "auto"),
            'support_url'               : app.config.get("support_url", "https://galaxyproject.org/support"),
            'search_url'                : app.config.get("search_url", "http://galaxyproject.org/search/"),
            'mailing_lists'             : app.config.get("mailing_lists", "https://galaxyproject.org/mailing-lists"),
            'screencasts_url'           : app.config.get("screencasts_url", "https://vimeo.com/galaxyproject"),
            'wiki_url'                  : app.config.get("wiki_url", "https://galaxyproject.org/"),
            'citation_url'              : app.config.get("citation_url", "https://galaxyproject.org/citing-galaxy"),
            'terms_url'                 : app.config.get("terms_url", ""),
=======
            'default_locale'            : app.config.default_locale,
            'support_url'               : app.config.support_url,
            'search_url'                : app.config.search_url,
            'mailing_lists'             : app.config.mailing_lists_url,
            'screencasts_url'           : app.config.screencasts_url,
            'wiki_url'                  : app.config.wiki_url,
            'citation_url'              : app.config.citation_url,
            'release_doc_base_url'      : app.config.release_doc_base_url,
            'terms_url'                 : app.config.terms_url or '',
>>>>>>> refs/heads/release_21.01
            'allow_user_creation'       : app.config.allow_user_creation,
            'logo_url'                  : h.url_for(app.config.logo_url),
            'logo_src'                  : h.url_for(app.config.get('logo_src', '/static/favicon.png')),
            'logo_src_secondary'        : h.url_for(app.config.get('logo_src_secondary')) if app.config.get('logo_src_secondary') else None,
            'is_admin_user'             : trans.user_is_admin,
            'active_view'               : active_view,
            'ftp_upload_site'           : app.config.ftp_upload_site,
            'datatypes_disable_auto'    : app.config.datatypes_disable_auto,
            'user_json'                 : get_user_dict()
        }
    %>

    ## load the frame manager
    <script type="text/javascript">
<<<<<<< HEAD

        // if we're in an iframe, create styles that hide masthead/messagebox, and reset top for panels
        // note: don't use a link to avoid roundtrip request
        // note: we can't select here because the page (incl. messgaebox, center, etc.) isn't fully rendered
        // TODO: remove these when we no longer navigate with iframes
        var in_iframe = window !== window.top;
        if( in_iframe ){
            var styleElement = document.createElement( 'style' );
            document.head.appendChild( styleElement );
            [
                '#masthead, #messagebox { display: none; }',
                '#center, #right, #left { top: 0 !important; }',
             ].forEach( function( rule ){
                styleElement.sheet.insertRule( rule, 0 );
            });
        }
        // TODO: ?? move above to base_panels.mako?
        $( function() {
            window.bundleEntries.masthead(${h.dumps(masthead_config)});
        });
=======
        if (window.self === window.top) {
            config.addInitialization(function (galaxy, config) {
                console.log("galaxy.masthead.mako", "initialize masthead");
                let options = ${h.dumps(masthead_config)};
                const container = document.getElementById("masthead");
                window.bundleEntries.initMasthead(options, container);
            });
        } else {
            console.log("galaxy.masthead.mako", "Detected embedding, not initializing masthead");
            const container = document.getElementById("masthead");
            container.parentNode.removeChild(container);
        }
>>>>>>> refs/heads/release_21.01
    </script>
</%def>
