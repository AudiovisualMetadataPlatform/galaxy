"""
Galaxy control queue and worker.  This is used to handle 'app' control like
reloading the toolbox, etc., across multiple processes.
"""

import importlib
import logging
import sys
import threading
import time
from inspect import ismodule
try:
    from math import inf
except ImportError:
    # python 2 doesn't have math.inf, but can use float('inf')
    inf = float('inf')

<<<<<<< HEAD
from kombu import Connection
from kombu.mixins import ConsumerMixin
from kombu.pools import producers
from six.moves import reload_module
=======
from kombu import (
    Consumer,
    Queue,
    uuid,
)
from kombu.mixins import ConsumerProducerMixin
from kombu.pools import (
    producers,
)
>>>>>>> refs/heads/release_21.01

import galaxy.queues
from galaxy import util
from galaxy.config import reload_config_options

logging.getLogger('kombu').setLevel(logging.WARNING)
log = logging.getLogger(__name__)


def send_local_control_task(app, task, get_response=False, kwargs=None):
    """
    This sends a message to the process-local control worker, which is useful
    for one-time asynchronous tasks like recalculating user disk usage.
    """
    if kwargs is None:
        kwargs = {}
    log.info("Queuing {} task {} for {}.".format("sync" if get_response else "async", task, app.config.server_name))
    payload = {'task': task,
               'kwargs': kwargs}
<<<<<<< HEAD
    try:
        c = Connection(app.config.amqp_internal_connection)
        with producers[c].acquire(block=True) as producer:
            producer.publish(payload,
                             exchange=galaxy.queues.galaxy_exchange,
                             declare=[galaxy.queues.galaxy_exchange] + [galaxy.queues.control_queue_from_config(app.config)],
                             routing_key='control.%s' % app.config.server_name)
    except Exception:
        log.exception("Error queueing async task: %s.", payload)
=======
    routing_key = f'control.{app.config.server_name}@{socket.gethostname()}'
    control_task = ControlTask(app.queue_worker)
    return control_task.send_task(payload, routing_key, local=True, get_response=get_response)
>>>>>>> refs/heads/release_21.01


<<<<<<< HEAD
def send_control_task(app, task, noop_self=False, kwargs={}):
=======
def send_control_task(app, task, noop_self=False, get_response=False, routing_key='control.*', kwargs=None):
>>>>>>> refs/heads/release_21.01
    """
    This sends a control task out to all processes, useful for things like
    reloading a data table, which needs to happen individually in all
    processes.
    """
    if kwargs is None:
        kwargs = {}
    log.info("Sending %s control task." % task)
    payload = {'task': task,
               'kwargs': kwargs}
    if noop_self:
        payload['noop'] = app.config.server_name
<<<<<<< HEAD
    try:
        c = Connection(app.config.amqp_internal_connection)
        with producers[c].acquire(block=True) as producer:
            control_queues = galaxy.queues.all_control_queues_for_declare(app.config, app.application_stack)
            producer.publish(payload, exchange=galaxy.queues.galaxy_exchange,
                             declare=[galaxy.queues.galaxy_exchange] + control_queues,
                             routing_key='control')
    except Exception:
        # This is likely connection refused.
        # TODO Use the specific Exception above.
        log.exception("Error sending control task: %s.", payload)
=======
    control_task = ControlTask(app.queue_worker)
    return control_task.send_task(payload=payload, routing_key=routing_key, get_response=get_response)


class ControlTask:

    def __init__(self, queue_worker):
        self.queue_worker = queue_worker
        self.correlation_id = None
        self.callback_queue = Queue(uuid(), exclusive=True, auto_delete=True)
        self.response = object()
        self._response = self.response
        self._connection = None

    @property
    def connection(self):
        if self._connection is None:
            self._connection = self.queue_worker.connection.clone()
        return self._connection

    @property
    def control_queues(self):
        return self.queue_worker.control_queues

    @property
    def exchange(self):
        return self.queue_worker.exchange_queue.exchange

    @property
    def declare_queues(self):
        return self.queue_worker.declare_queues

    def on_response(self, message):
        if message.properties['correlation_id'] == self.correlation_id:
            self.response = message.payload['result']

    def send_task(self, payload, routing_key, local=False, get_response=False, timeout=10):
        if local:
            declare_queues = self.control_queues
        else:
            declare_queues = self.declare_queues
        reply_to = None
        callback_queue = []
        if get_response:
            reply_to = self.callback_queue.name
            callback_queue = [self.callback_queue]
            self.correlation_id = uuid()
        try:
            with producers[self.connection].acquire(block=True, timeout=10) as producer:
                producer.publish(
                    payload,
                    exchange=None if local else self.exchange,
                    declare=declare_queues,
                    routing_key=routing_key,
                    reply_to=reply_to,
                    correlation_id=self.correlation_id,
                    retry=True,
                    headers={'epoch': time.time()},
                )
            if get_response:
                with Consumer(self.connection, on_message=self.on_response, queues=callback_queue, no_ack=True):
                    while self.response is self._response:
                        self.connection.drain_events(timeout=timeout)
                return self.response
        except socket.timeout:
            log.exception("Error waiting for task: '%s' sent with routing key '%s'", payload, routing_key)
        except Exception:
            log.exception("Error queueing async task: '%s'. for %s", payload, routing_key)
>>>>>>> refs/heads/release_21.01


# Tasks -- to be reorganized into a separate module as appropriate.  This is
# just an example method.  Ideally this gets pushed into atomic tasks, whether
# where they're currently invoked, or elsewhere.  (potentially using a dispatch
# decorator).

def reconfigure_watcher(app, **kwargs):
    app.database_heartbeat.update_watcher_designation()


def create_panel_section(app, **kwargs):
    """
    Updates in memory toolbox dictionary.
    """
    log.debug("Updating in-memory tool panel")
    app.toolbox.create_section(kwargs)


def reload_tool(app, **kwargs):
    params = util.Params(kwargs)
    tool_id = params.get('tool_id', None)
    log.debug("Executing reload tool task for %s" % tool_id)
    if tool_id:
        app.toolbox.reload_tool_by_id(tool_id)
    else:
        log.error("Reload tool invoked without tool id.")


def reload_toolbox(app, save_integrated_tool_panel=True, **kwargs):
    reload_timer = util.ExecutionTimer()
    log.debug("Executing toolbox reload on '%s'", app.config.server_name)
    reload_count = app.toolbox._reload_count
    if hasattr(app, 'tool_cache'):
        app.tool_cache.cleanup()
    _get_new_toolbox(app, save_integrated_tool_panel)
    app.toolbox._reload_count = reload_count + 1
    send_local_control_task(app, 'rebuild_toolbox_search_index')
    log.debug("Toolbox reload %s", reload_timer)


def _get_new_toolbox(app, save_integrated_tool_panel=True):
    """
    Generate a new toolbox, by constructing a toolbox from the config files,
    and then adding pre-existing data managers from the old toolbox to the new toolbox.
    """
    from galaxy import tools
    from galaxy.tools.special_tools import load_lib_tools
    if hasattr(app, 'tool_shed_repository_cache'):
        app.tool_shed_repository_cache.rebuild()
    tool_configs = app.config.tool_configs

    new_toolbox = tools.ToolBox(tool_configs, app.config.tool_path, app, save_integrated_tool_panel=save_integrated_tool_panel)
    new_toolbox.data_manager_tools = app.toolbox.data_manager_tools
    app.datatypes_registry.load_datatype_converters(new_toolbox, use_cached=True)
    app.datatypes_registry.load_external_metadata_tool(new_toolbox)
    load_lib_tools(new_toolbox)
    [new_toolbox.register_tool(tool) for tool in new_toolbox.data_manager_tools.values()]
    app.toolbox = new_toolbox
    app.toolbox.persist_cache()


def reload_data_managers(app, **kwargs):
    reload_timer = util.ExecutionTimer()
    from galaxy.tools.data_manager.manager import DataManagers
    log.debug("Executing data managers reload on '%s'", app.config.server_name)
    if hasattr(app, 'tool_shed_repository_cache'):
        app.tool_shed_repository_cache.rebuild()
    app._configure_tool_data_tables(from_shed_config=False)
    reload_tool_data_tables(app)
    reload_count = app.data_managers._reload_count
    app.data_managers = DataManagers(app)
    app.data_managers._reload_count = reload_count + 1
    if hasattr(app, 'tool_cache'):
        app.tool_cache.reset_status()
    if hasattr(app, 'watchers'):
        app.watchers.update_watch_data_table_paths()
    log.debug("Data managers reloaded %s", reload_timer)


def reload_display_application(app, **kwargs):
    display_application_ids = kwargs.get('display_application_ids', None)
    log.debug("Executing display application reload task for %s" % display_application_ids)
    app.datatypes_registry.reload_display_applications(display_application_ids)


def reload_sanitize_allowlist(app):
    log.debug("Executing reload sanitize allowlist control task.")
    app.config.reload_sanitize_allowlist()


def recalculate_user_disk_usage(app, **kwargs):
    user_id = kwargs.get('user_id', None)
    sa_session = app.model.context
    if user_id:
        user = sa_session.query(app.model.User).get(app.security.decode_id(user_id))
        if user:
            user.calculate_and_set_disk_usage()
        else:
            log.error("Recalculate user disk usage task failed, user %s not found" % user_id)
    else:
        log.error("Recalculate user disk usage task received without user_id.")


def reload_tool_data_tables(app, **kwargs):
    path = kwargs.get('path')
    table_name = kwargs.get('table_name')
    table_names = path or table_name or 'all tables'
    log.debug("Executing tool data table reload for %s", table_names)
    table_names = app.tool_data_tables.reload_tables(table_names=table_name, path=path)
    log.debug("Finished data table reload for %s", table_names)


def rebuild_toolbox_search_index(app, **kwargs):
    if app.is_webapp:
        if app.toolbox_search.index_count < app.toolbox._reload_count:
            app.reindex_tool_search()
    else:
        log.debug("App is not a webapp, not building a search index")


def reload_job_rules(app, **kwargs):
    reload_timer = util.ExecutionTimer()
    for module in job_rule_modules(app):
        rules_module_name = module.__name__
        for name, module in sys.modules.items():
            if ((name == rules_module_name or name.startswith(rules_module_name + '.'))
                    and ismodule(module)):
                log.debug("Reloading job rules module: %s", name)
                importlib.reload(module)
    log.debug("Job rules reloaded %s", reload_timer)


def reload_core_config(app, **kwargs):
    reload_config_options(app.config)


def reload_tour(app, **kwargs):
    path = kwargs.get('path')
    app.tour_registry.reload_tour(path)
    log.debug('Tour reloaded')


def __job_rule_module_names(app):
    rules_module_names = {'galaxy.jobs.rules'}
    if app.job_config.dynamic_params is not None:
        module_name = app.job_config.dynamic_params.get('rules_module')
        if module_name:
            rules_module_names.add(module_name)
    # Also look for destination level rules_module overrides
    for dest_tuple in app.job_config.destinations.values():
        module_name = dest_tuple[0].params.get('rules_module')
        if module_name:
            rules_module_names.add(module_name)
    return rules_module_names


def job_rule_modules(app):
    rules_module_list = []
    for rules_module_name in __job_rule_module_names(app):
        rules_module = sys.modules.get(rules_module_name, None)
        if not rules_module:
            # if using a non-default module, it's not imported until a JobRunnerMapper is instantiated when the first
            # JobWrapper is created
            rules_module = importlib.import_module(rules_module_name)
        rules_module_list.append(rules_module)
    return rules_module_list


def admin_job_lock(app, **kwargs):
    job_lock = kwargs.get('job_lock', False)
    # job_queue is exposed in the root app, but this will be 'fixed' at some
    # point, so we're using the reference from the handler.
    app.job_manager.job_lock = job_lock
    log.info("Administrative Job Lock is now set to %s. Jobs will %s dispatch."
             % (job_lock, "not" if job_lock else "now"))


control_message_to_task = {
    'create_panel_section': create_panel_section,
    'reload_tool': reload_tool,
    'reload_toolbox': reload_toolbox,
    'reload_data_managers': reload_data_managers,
    'reload_display_application': reload_display_application,
    'reload_tool_data_tables': reload_tool_data_tables,
    'reload_job_rules': reload_job_rules,
    'admin_job_lock': admin_job_lock,
    'reload_sanitize_allowlist': reload_sanitize_allowlist,
    'recalculate_user_disk_usage': recalculate_user_disk_usage,
    'rebuild_toolbox_search_index': rebuild_toolbox_search_index,
    'reconfigure_watcher': reconfigure_watcher,
    'reload_tour': reload_tour,
    'reload_core_config': reload_core_config,
}


class GalaxyQueueWorker(ConsumerMixin, threading.Thread):
    """
    This is a flexible worker for galaxy's queues.  Each process, web or
    handler, will have one of these used for dispatching so called 'control'
    tasks.
    """

<<<<<<< HEAD
    def __init__(self, app, queue=None, task_mapping=control_message_to_task, connection=None):
        super(GalaxyQueueWorker, self).__init__()
=======
    def __init__(self, app, task_mapping=None):
        super().__init__()
>>>>>>> refs/heads/release_21.01
        log.info("Initializing %s Galaxy Queue Worker on %s", app.config.server_name, util.mask_password_from_url(app.config.amqp_internal_connection))
        self.daemon = True
        if connection:
            self.connection = connection
        else:
            self.connection = app.amqp_internal_connection_obj
        # explicitly force connection instead of lazy-connecting the first
        # time it is required.
        self.connection.connect()
        self.app = app
<<<<<<< HEAD
        # Eventually we may want different workers w/ their own queues and task
        # mappings.  Right now, there's only the one.
        if queue:
            # Allows assignment of a particular queue for this worker.
            self.control_queue = queue
        else:
            # Default to figuring out which control queue to use based on the app config.
            queue = galaxy.queues.control_queue_from_config(app.config)
        self.task_mapping = task_mapping
        self.declare_queues = galaxy.queues.all_control_queues_for_declare(app.config, app.application_stack)
        # TODO we may want to purge the queue at the start to avoid executing
        # stale 'reload_tool', etc messages.  This can happen if, say, a web
        # process goes down and messages get sent before it comes back up.
        # Those messages will no longer be useful (in any current case)
=======
        self.task_mapping = task_mapping or control_message_to_task
        self.exchange_queue = None
        self.direct_queue = None
        self.control_queues = []
        self.epoch = 0

    def send_control_task(self, task, noop_self=False, get_response=False, routing_key='control.*', kwargs=None):
        return send_control_task(app=self.app, task=task, noop_self=noop_self, get_response=get_response, routing_key=routing_key, kwargs=kwargs)

    def send_local_control_task(self, task, get_response=False, kwargs=None):
        return send_local_control_task(app=self.app, get_response=get_response, task=task, kwargs=kwargs)

    @property
    def declare_queues(self):
        # dynamically produce queues, allows addressing all known processes at a given time
        return galaxy.queues.all_control_queues_for_declare(self.app.application_stack)
>>>>>>> refs/heads/release_21.01

    def bind_and_start(self):
        log.info("Binding and starting galaxy control worker for %s", self.app.config.server_name)
<<<<<<< HEAD
        self.control_queue = galaxy.queues.control_queue_from_config(self.app.config)
=======
        self.exchange_queue, self.direct_queue = galaxy.queues.control_queues_from_config(self.app.config)
        self.control_queues = [self.exchange_queue, self.direct_queue]
        self.epoch = time.time()
>>>>>>> refs/heads/release_21.01
        self.start()

    def get_consumers(self, Consumer, channel):
        return [Consumer(queues=self.control_queue,
                         callbacks=[self.process_task])]

    def process_task(self, body, message):
        if body['task'] in self.task_mapping:
            if body.get('noop', None) != self.app.config.server_name:
                try:
                    f = self.task_mapping[body['task']]
<<<<<<< HEAD
                    log.info("Instance '%s' received '%s' task, executing now.", self.app.config.server_name, body['task'])
                    f(self.app, **body['kwargs'])
=======
                    if message.headers.get('epoch', inf) > self.epoch:
                        # Message was created after QueueWorker was started, execute
                        log.info("Instance '%s' received '%s' task, executing now.", self.app.config.server_name, body['task'])
                        result = f(self.app, **body['kwargs'])
                    else:
                        # Message was created before QueueWorker was started, ack message but don't run task
                        log.info("Instance '%s' received '%s' task from the past, discarding it", self.app.config.server_name, body['task'])
                        result = 'NO_OP'
>>>>>>> refs/heads/release_21.01
                except Exception:
                    # this shouldn't ever throw an exception, but...
                    log.exception("Error running control task type: %s", body['task'])
        else:
            log.warning("Received a malformed task message:\n%s" % body)
        message.ack()

    def shutdown(self):
        self.should_stop = True
        self.join()
