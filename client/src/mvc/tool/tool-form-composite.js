/** This is the run workflow tool form view. */
import _ from "underscore";
import $ from "jquery";
import Backbone from "backbone";
import { getAppRoot } from "onload/loadConfig";
import { getGalaxyInstance } from "app";
import _l from "utils/localization";
import Utils from "utils/utils";
import Deferred from "utils/deferred";
import Form from "mvc/form/form-view";
import { isDataStep, invokeWorkflow } from "components/Workflow/Run";

import ToolFormBase from "mvc/tool/tool-form-base";
import Modal from "mvc/ui/ui-modal";

var View = Backbone.View.extend({
    initialize: function (options) {
        const Galaxy = getGalaxyInstance();
        this.modal = Galaxy.modal || new Modal.View();
        this.runWorkflowModel = options.model;
        this.deferred = new Deferred();
        this.setRunButtonStatus = options.setRunButtonStatus;
        this.handleInvocations = options.handleInvocations;
        this.setElement(options.el);
        this._configure();
        this.render();
    },

    /** Configures form/step options for each workflow step */
    _configure: function () {
        this.forms = [];
        this.steps = this.runWorkflowModel.steps;
        this.links = this.runWorkflowModel.links;
        this.parms = this.runWorkflowModel.parms;
        this.wp_inputs = this.runWorkflowModel.wpInputs;
    },

    render: function () {
        this.deferred.reset();
        this._renderParameters();
        this._renderHistory();
        this._renderUseCachedJob();
        this._renderResourceParameters();
        _.each(this.steps, (step) => {
            this._renderStep(step);
        });
    },

    /** Render workflow parameters */
    _renderParameters: function () {
        this.wp_form = null;
        if (!_.isEmpty(this.wp_inputs)) {
            this.wp_form = new Form({
                title: "<b>Workflow Parameters</b>",
                inputs: this.wp_inputs,
                cls: "ui-portlet-section",
                onchange: () => {
                    _.each(this.wp_form.input_list, (input_def, i) => {
                        _.each(input_def.links, (step) => {
                            this._refreshStep(step);
                        });
                    });
                },
            });
            this._append(this.$el.empty(), this.wp_form.$el);
        }
    },

    /** Render workflow parameters */
    _renderHistory: function () {
        this.history_form = new Form({
            cls: "ui-portlet-section",
            title: "<b>History Options</b>",
            inputs: [
                {
                    type: "conditional",
                    name: "new_history",
                    test_param: {
                        name: "check",
                        label: "Send results to a new history",
                        type: "boolean",
                        value: "false",
                        help: "",
                    },
                    cases: [
                        {
                            value: "true",
                            inputs: [
                                {
                                    name: "name",
                                    label: "History name",
                                    type: "text",
                                    value: this.runWorkflowModel.name,
                                },
                            ],
                        },
                    ],
                },
            ],
        });
        this._append(this.$el, this.history_form.$el);
    },

    /** Render Workflow Options */
    _renderResourceParameters: function () {
        this.workflow_resource_parameters_form = null;
        if (!_.isEmpty(this.runWorkflowModel.workflowResourceParameters)) {
            this.workflow_resource_parameters_form = new Form({
                cls: "ui-portlet-section",
                title: "<b>Workflow Resource Options</b>",
                inputs: this.runWorkflowModel.workflowResourceParameters,
            });
            this._append(this.$el, this.workflow_resource_parameters_form.$el);
        }
    },

    /** Render job caching option */
    _renderUseCachedJob: function () {
        const Galaxy = getGalaxyInstance();
        var extra_user_preferences = {};
        if (Galaxy.user.attributes.preferences && "extra_user_preferences" in Galaxy.user.attributes.preferences) {
            extra_user_preferences = JSON.parse(Galaxy.user.attributes.preferences.extra_user_preferences);
        }
        var display_use_cached_job_checkbox =
            "use_cached_job|use_cached_job_checkbox" in extra_user_preferences
                ? extra_user_preferences["use_cached_job|use_cached_job_checkbox"]
                : false;
        this.display_use_cached_job_checkbox = display_use_cached_job_checkbox === "true";
        if (this.display_use_cached_job_checkbox) {
            this.job_options_form = new Form({
                cls: "ui-portlet-section",
                title: "<b>Job re-use Options</b>",
                inputs: [
                    {
                        type: "conditional",
                        name: "use_cached_job",
                        test_param: {
                            name: "check",
                            label: "BETA: Attempt to reuse jobs with identical parameters?",
                            type: "boolean",
                            value: "false",
                            help: "This may skip executing jobs that you have already run.",
                        },
                    },
                ],
            });
            this._append(this.$el, this.job_options_form.$el);
        }
    },

    /** Render step */
    _renderStep: function (step) {
        const Galaxy = getGalaxyInstance();
        var form = null;
        this.deferred.execute((promise) => {
            this.$el.addClass("ui-steps");
            if (step.step_type == "tool") {
                step.postchange = function (process, form) {
                    var current_state = {
                        tool_id: step.id,
                        tool_version: step.version,
                        inputs: $.extend(true, {}, form.data.create()),
                    };
                    form.wait(true);
                    Galaxy.emit.debug("tool-form-composite::postchange()", "Sending current state.", current_state);
                    Utils.request({
                        type: "POST",
                        url: `${getAppRoot()}api/tools/${step.id}/build`,
                        data: current_state,
                        success: function (data) {
                            form.update(data);
                            form.wait(false);
                            Galaxy.emit.debug("tool-form-composite::postchange()", "Received new model.", data);
                            process.resolve();
                        },
                        error: function (response) {
                            Galaxy.emit.debug("tool-form-composite::postchange()", "Refresh request failed.", response);
                            process.reject();
                        },
                    });
                };
                form = new ToolFormBase(step);
                if (step.post_job_actions && step.post_job_actions.length) {
                    form.portlet.append(
                        $("<div/>")
                            .addClass("ui-form-element-disabled")
                            .append($("<div/>").addClass("ui-form-title").html("<b>Job Post Actions</b>"))
                            .append(
                                $("<div/>")
                                    .addClass("ui-form-preview")
                                    .html(
                                        _.reduce(
                                            step.post_job_actions,
                                            (memo, value) => `${memo} ${value.short_str}`,
                                            ""
                                        )
                                    )
                            )
                    );
                }
            } else {
                var is_simple_input = ["data_input", "data_collection_input"].indexOf(step.step_type) != -1;
                _.each(step.inputs, (input) => {
                    input.flavor = "module";
                    input.hide_label = is_simple_input;
                });
                form = new Form(
                    Utils.merge(
                        {
                            title: step.fixed_title,
                            onchange: () => {
                                _.each(this.links[step.index], (link) => {
                                    this._refreshStep(link);
                                });
                            },
                            inputs:
                                step.inputs && step.inputs.length > 0
                                    ? step.inputs
                                    : [
                                          {
                                              type: "hidden",
                                              name: "No options available.",
                                              ignore: null,
                                          },
                                      ],
                        },
                        step
                    )
                );
                if (step.step_label) {
                    form.$el.attr("step-label", step.step_label);
                }
            }
            this.forms[step.index] = form;
            this._append(this.$el, form.$el);
            if (step.needs_refresh) {
                this._refreshStep(step);
            }
            form.portlet[!this.show_progress ? "enable" : "disable"]();
            if (this.show_progress) {
                const percentage = ((step.index + 1) * 100.0) / this.steps.length;
                this.setRunButtonStatus(false, "Preparing...", percentage);
            }
            Galaxy.emit.debug("tool-form-composite::initialize()", `${step.index} : Workflow step state ready.`, step);
            window.setTimeout(() => {
                promise.resolve();
            }, 0);
        });
    },

    /** Refreshes step values from source step values */
    _refreshStep: function (step) {
        var form = this.forms[step.index];
        if (form) {
            _.each(this.parms[step.index], (input, name) => {
                if (input.step_linked || input.wp_linked) {
                    var field = form.field_list[form.data.match(name)];
                    if (field) {
                        var new_value;
                        if (input.step_linked) {
                            new_value = { values: [] };
                            _.each(input.step_linked, (source_step) => {
                                if (isDataStep(source_step)) {
                                    var value = this.forms[source_step.index].data.create().input;
                                    if (value) {
                                        _.each(value.values, (v) => {
                                            new_value.values.push(v);
                                        });
                                    }
                                }
                            });
                            if (!input.multiple && new_value.values.length > 0) {
                                new_value = {
                                    values: [new_value.values[0]],
                                };
                            }
                        } else if (input.wp_linked) {
                            new_value = input.value;
                            var re = /\$\{(.+?)\}/g;
                            var match;
                            while ((match = re.exec(input.value))) {
                                var wp_field = this.wp_form.field_list[this.wp_form.data.match(match[1])];
                                var wp_value = wp_field && wp_field.value();
                                if (wp_value) {
                                    new_value = new_value.split(match[0]).join(wp_value);
                                }
                            }
                        }
                        if (new_value !== undefined) {
                            field.value(new_value);
                        }
                    }
                }
            });
            form.trigger("change");
        } else {
            step.needs_refresh = true;
        }
    },

    /** Build remaining steps */
    execute: function () {
        this.show_progress = true;
        this._enabled(false);
        this.deferred.execute((promise) => {
            window.setTimeout(() => {
                promise.resolve();
                this._submit();
            }, 0);
        });
    },

    /** Validate and submit workflow */
    _submit: function () {
        const Galaxy = getGalaxyInstance();
        var history_form_data = this.history_form.data.create();
        var job_def = {
            new_history_name: history_form_data["new_history|name"] ? history_form_data["new_history|name"] : null,
            history_id: !history_form_data["new_history|name"] ? this.runWorkflowModel.historyId : null,
            resource_params: this.workflow_resource_parameters_form
                ? this.workflow_resource_parameters_form.data.create()
                : {},
            replacement_params: this.wp_form ? this.wp_form.data.create() : {},
            parameters: {},
            // Tool form will submit flat maps for each parameter
            // (e.g. "repeat_0|cond|param": "foo" instead of nested
            // data structures).
            parameters_normalized: true,
            // Tool form always wants a list of invocations back
            // so that inputs can be batched.
            batch: true,
        };
        if (this.display_use_cached_job_checkbox) {
            job_def.use_cached_job = this.job_options_form.data.create()["use_cached_job|check"] === "true";
        }
        var validated = true;
        for (var i in this.forms) {
            var form = this.forms[i];
            var job_inputs = form.data.create();
            var step = this.steps[i];
            var step_index = step.step_index;
            form.trigger("reset");
            for (var job_input_id in job_inputs) {
                var input_value = job_inputs[job_input_id];
                var input_id = form.data.match(job_input_id);
                var input_def = form.input_list[input_id];
                if (!input_def.step_linked) {
                    if (isDataStep(step)) {
                        validated = input_value && input_value.values && input_value.values.length > 0;
                        if (!validated && input_def.optional) {
                            validated = true;
                        }
                    } else {
                        validated =
                            input_def.optional ||
                            (input_def.is_workflow && input_value !== "") ||
                            (!input_def.is_workflow && input_value !== null);
                    }
                    if (!validated) {
                        if (input_def.type == "hidden") {
                            this.modal.show({
                                title: _l("Workflow submission failed"),
                                body: `Step ${step_index}: ${
                                    step.step_label || step.step_name
                                } is in an invalid state. Please remove and re-add this step in the Workflow Editor.`,
                                buttons: {
                                    Close: () => {
                                        this.modal.hide();
                                    },
                                },
                            });
                        }
                        form.highlight(input_id);
                        break;
                    }
                    job_def.parameters[step_index] = job_def.parameters[step_index] || {};
                    job_def.parameters[step_index][job_input_id] = job_inputs[job_input_id];
                }
            }
            if (!validated) {
                break;
            }
        }
        if (!validated) {
            this._enabled(true);
            Galaxy.emit.debug("tool-form-composite::submit()", "Validation failed.", job_def);
        } else {
            Galaxy.emit.debug("tool-form-composite::submit()", "Validation complete.", job_def);
            invokeWorkflow(this.runWorkflowModel.workflowId, job_def)
                .then((invocations) => {
                    Galaxy.emit.debug("tool-form-composite::submit", "Submission successful.", invocations);
                    if ($.isArray(invocations) && invocations.length > 0) {
                        this.handleInvocations(invocations);
                    } else {
                        this.submissionErrorModal(job_def, invocations);
                    }
                    this._enabled(true);
                })
                .catch((response) => {
                    // TODO: Is this the same response as the Utils post would
                    // have had?
                    Galaxy.emit.debug("tool-form-composite::submit", "Submission failed.", response);
                    var input_found = false;
                    if (response && response.err_data) {
                        for (var i in this.forms) {
                            var form = this.forms[i];
                            var step_related_errors = response.err_data[form.model.get("step_index")];
                            if (step_related_errors) {
                                var error_messages = form.data.matchResponse(step_related_errors);
                                for (var input_id in error_messages) {
                                    form.highlight(input_id, error_messages[input_id]);
                                    input_found = true;
                                    break;
                                }
                            }
                        }
                    }
                    if (!input_found) {
                        this.submissionErrorModal(job_def, response);
                    }
                    this._enabled(true);
                });
        }
    },

    /** Append new dom to body */
    _append: function ($container, $el) {
        $container.append("<p/>").append($el);
    },

    /** Set enabled/disabled state */
    _enabled: function (enabled) {
        this.setRunButtonStatus(enabled, "Sending...", -1);
        if (this.wp_form) {
            this.wp_form.portlet[enabled ? "enable" : "disable"]();
        }
        if (this.history_form) {
            this.history_form.portlet[enabled ? "enable" : "disable"]();
        }
        _.each(this.forms, (form) => {
            if (form) {
                form.portlet[enabled ? "enable" : "disable"]();
            }
        });
    },

    submissionErrorModal: function (job_def, response) {
        this.modal.show({
            title: _l("Workflow submission failed"),
            body: this._templateError(job_def, response && response.err_msg),
            buttons: {
                Close: () => {
                    this.modal.hide();
                },
            },
        });
    },

    /** Templates */
    _templateError: function (response, err_msg) {
        return $("<div/>")
            .addClass("errormessagelarge")
            .append(
                $("<p/>").text(
                    `The server could not complete the request. Please contact the Galaxy Team if this error persists. ${
                        JSON.stringify(err_msg) || ""
                    }`
                )
            )
            .append($("<pre/>").text(JSON.stringify(response, null, 4)));
    },
});
export default {
    View: View,
};
