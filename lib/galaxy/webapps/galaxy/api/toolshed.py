import json
import logging
from urllib.parse import quote

<<<<<<< HEAD
from six.moves.urllib.parse import (
    quote as urlquote,
    unquote as urlunquote
)

from galaxy import (
    util,
    web
)
from galaxy.web import _future_expose_api as expose_api
from galaxy.web.base.controller import BaseAPIController
from tool_shed.util import (
    common_util,
    repository_util,
    tool_util
)
=======
from galaxy.exceptions import MessageException
from galaxy.util import url_get
from galaxy.web import expose_api, require_admin
from galaxy.webapps.base.controller import BaseAPIController
>>>>>>> refs/heads/release_21.01

log = logging.getLogger(__name__)


class ToolShedController(BaseAPIController):
    """RESTful controller for interactions with Toolsheds."""

    @expose_api
    def index(self, trans, **kwd):
        """
        GET /api/tool_shed
        Interact with the Toolshed registry of this instance.
        """
        tool_sheds = []
        for name, url in trans.app.tool_shed_registry.tool_sheds.items():
            tool_sheds.append(dict(name=name, url=quote(url, '')))
        return tool_sheds

    @require_admin
    @expose_api
    def request(self, trans, **params):
        """
        GET /api/tool_shed/request
        """
        tool_shed_url = params.pop("tool_shed_url")
        controller = params.pop("controller")
        if controller is None:
            raise MessageException("Please provide a toolshed controller name.")
        tool_shed_registry = trans.app.tool_shed_registry
        if tool_shed_registry is None:
            raise MessageException("Toolshed registry not available.")
        if tool_shed_url in tool_shed_registry.tool_sheds.values():
            pathspec = ["api", controller]
            if "id" in params:
                pathspec.append(params.pop("id"))
            if "action" in params:
                pathspec.append(params.pop("action"))
            try:
                return json.loads(url_get(tool_shed_url, params=dict(params), pathspec=pathspec))
            except Exception as e:
                raise MessageException("Invalid server response. %s." % str(e))
        else:
<<<<<<< HEAD
            return []
        # return tool_shed_repository_dict

    @expose_api
    @web.require_admin
    def tool_json(self, trans, **kwd):
        """
        GET /api/tool_shed_repositories/shed_tool_json

        Get the tool form JSON for a tool in a toolshed repository.

        :param guid:          the GUID of the tool
        :param guid:          str

        :param tsr_id:        the ID of the repository
        :param tsr_id:        str

        :param changeset:        the changeset at which to load the tool json
        :param changeset:        str

        :param tool_shed_url:   the URL of the toolshed to load from
        :param tool_shed_url:   str
        """
        tool_shed_url = kwd.get('tool_shed_url', None)
        tsr_id = kwd.get('tsr_id', None)
        guid = kwd.get('guid', None)
        changeset = kwd.get('changeset', None)
        if None in [tool_shed_url, tsr_id, guid, changeset]:
            message = 'Tool shed URL, changeset, repository ID, and tool GUID are all required parameters.'
            trans.response.status = 400
            return {'status': 'error', 'message': message}
        response = json.loads(util.url_get(tool_shed_url, params=dict(tsr_id=tsr_id, guid=guid, changeset=changeset.split(':')[-1]), pathspec=['api', 'tools', 'json']))
        return response

    @expose_api
    def show(self, trans, **kwd):
        """
        GET /api/tool_shed/contents

        Display a list of categories in the selected toolshed.

        :param tool_shed_url: the url of the toolshed to get categories from
        """
        tool_shed_url = urlunquote(kwd.get('tool_shed_url', ''))
        tool_shed_url = common_util.get_tool_shed_url_from_tool_shed_registry(trans.app, tool_shed_url)
        url = util.build_url(tool_shed_url, pathspec=['api', 'categories'])
        categories = []
        for category in json.loads(util.url_get(url)):
            api_url = web.url_for(controller='api/tool_shed',
                                  action='category',
                                  tool_shed_url=urlquote(tool_shed_url),
                                  category_id=category['id'],
                                  qualified=True)
            category['url'] = api_url
            categories.append(category)
        return categories

    @expose_api
    @web.require_admin
    def category(self, trans, **kwd):
        """
        GET /api/tool_shed/category

        Display a list of repositories in the selected category.

        :param tool_shed_url: the url of the toolshed to get repositories from
        :param category_id: the category to get repositories from
        """
        tool_shed_url = urlunquote(kwd.get('tool_shed_url', ''))
        category_id = kwd.get('category_id', '')
        params = dict(installable=True)
        tool_shed_url = common_util.get_tool_shed_url_from_tool_shed_registry(trans.app, tool_shed_url)
        url = util.build_url(tool_shed_url, pathspec=['api', 'categories', category_id, 'repositories'], params=params)
        repositories = []
        return_json = json.loads(util.url_get(url))
        for repository in return_json['repositories']:
            api_url = web.url_for(controller='api/tool_shed',
                                  action='repository',
                                  tool_shed_url=urlquote(tool_shed_url),
                                  repository_id=repository['id'],
                                  qualified=True)
            repository['url'] = api_url
            repositories.append(repository)
        return_json['repositories'] = repositories
        return return_json

    @expose_api
    def repository(self, trans, **kwd):
        """
        GET /api/tool_shed/repository

        Get details about the specified repository from its shed.

        :param repository_id:          the tool_shed_repository_id
        :param repository_id:          str

        :param tool_shed_url:   the URL of the toolshed whence to retrieve repository details
        :param tool_shed_url:   str

        :param tool_ids:         (optional) comma-separated list of tool IDs
        :param tool_ids:         str
        """
        tool_dependencies = dict()
        tools = dict()
        tool_shed_url = urlunquote(kwd.get('tool_shed_url', ''))
        log.debug(tool_shed_url)
        repository_id = kwd.get('repository_id', None)
        tool_ids = kwd.get('tool_ids', None)
        if tool_ids is not None:
            tool_ids = util.listify(tool_ids)
        tool_panel_section_select_field = tool_util.build_tool_panel_section_select_field(trans.app)
        tool_panel_section_dict = {'name': tool_panel_section_select_field.name,
                                   'id': tool_panel_section_select_field.field_id,
                                   'sections': []}
        for name, id, _ in tool_panel_section_select_field.options:
            tool_panel_section_dict['sections'].append(dict(id=id, name=name))
        repository_data = dict()
        if tool_ids is not None:
            if len(tool_shed_url) == 0:
                # By design, this list should always be from the same toolshed. If
                # this is ever not the case, this code will need to be updated.
                tool_shed_url = common_util.get_tool_shed_url_from_tool_shed_registry(self.app, tool_ids[0].split('/repos')[0])
            found_repository = json.loads(util.url_get(tool_shed_url, params=dict(tool_ids=','.join(tool_ids)), pathspec=['api', 'repositories']))
            current_changeset = found_repository['current_changeset']
            repository_id = found_repository[current_changeset]['repository_id']
            repository_data['current_changeset'] = current_changeset
            repository_data['repository'] = json.loads(util.url_get(tool_shed_url, pathspec=['api', 'repositories', repository_id]))
            del found_repository['current_changeset']
            repository_data['tool_shed_url'] = tool_shed_url
        else:
            repository_data['repository'] = json.loads(util.url_get(tool_shed_url, pathspec=['api', 'repositories', repository_id]))
        repository_data['repository']['metadata'] = json.loads(util.url_get(tool_shed_url, pathspec=['api', 'repositories', repository_id, 'metadata']))
        repository_data['shed_conf'] = tool_util.build_shed_tool_conf_select_field(trans.app).to_dict()
        repository_data['panel_section_dict'] = tool_panel_section_dict
        for changeset, metadata in repository_data['repository']['metadata'].items():
            if changeset not in tool_dependencies:
                tool_dependencies[changeset] = []
            if metadata['includes_tools_for_display_in_tool_panel']:
                if changeset not in tools:
                    tools[changeset] = []
                for tool_dict in metadata['tools']:
                    tool_info = dict(clean=re.sub('[^a-zA-Z0-9]+', '_', tool_dict['name']).lower(),
                                     guid=tool_dict['guid'],
                                     name=tool_dict['name'],
                                     version=tool_dict['version'],
                                     description=tool_dict['description'])
                    if tool_info not in tools[changeset]:
                        tools[changeset].append(tool_info)
                if metadata['has_repository_dependencies']:
                    for repository_dependency in metadata['repository_dependencies']:
                        tools[changeset] = self.__get_tools(repository_dependency, tools[changeset])
            for key, dependency_dict in metadata['tool_dependencies'].items():
                if 'readme' in dependency_dict:
                    del(dependency_dict['readme'])
                if dependency_dict not in tool_dependencies[changeset]:
                    tool_dependencies[changeset].append(dependency_dict)
            if metadata['has_repository_dependencies']:
                for repository_dependency in metadata['repository_dependencies']:
                    tool_dependencies[changeset] = self.__get_tool_dependencies(repository_dependency, tool_dependencies[changeset])
        for changeset in repository_data['repository']['metadata']:
            if changeset in tools:
                repository_data['repository']['metadata'][changeset]['tools'] = tools[changeset]
            else:
                repository_data['repository']['metadata'][changeset]['tools'] = []
        repository_data['tool_dependencies'] = tool_dependencies
        return repository_data

    @expose_api
    @web.require_admin
    def search(self, trans, **kwd):
        """
        GET /api/tool_shed/search
        Search for a specific repository in the toolshed.
        :param q:          the query string to search for
        :param q:          str
        :param tool_shed_url:   the URL of the toolshed to search
        :param tool_shed_url:   str
        """
        tool_shed_url = kwd.get('tool_shed_url', None)
        q = kwd.get('term', None)
        if None in [q, tool_shed_url]:
            return {}
        response = json.loads(util.url_get(tool_shed_url, params=dict(q=q), pathspec=['api', 'repositories']))
        return response
=======
            raise MessageException("Invalid toolshed url.")
>>>>>>> refs/heads/release_21.01
