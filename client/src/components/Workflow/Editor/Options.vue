<template>
    <div class="panel-header-buttons">
        <b-button
            id="workflow-home-button"
            role="button"
            title="Edit Attributes"
            variant="link"
            aria-label="Edit Attributes"
            class="editor-button-attributes"
            v-b-tooltip.hover
            @click="$emit('onAttributes')"
        >
            <span class="fa fa-pencil-alt" />
        </b-button>
        <b-button
            id="workflow-save-button"
            role="button"
            title="Save Workflow"
            variant="link"
            aria-label="Save Workflow"
            class="editor-button-save"
            :disabled="!hasChanges"
            v-b-tooltip.hover
            @click="$emit('onSave')"
        >
            <span class="fa fa-floppy-o" />
        </b-button>
        <b-button
            id="workflow-report-button"
            role="button"
            title="Edit Report"
            variant="link"
            aria-label="Edit Report"
            class="editor-button-report"
            v-b-tooltip.hover
            @click="$emit('onReport')"
        >
            <span class="fa fa-edit" />
        </b-button>
        <b-dropdown
            no-caret
            right
            id="workflow-options-button"
            role="button"
            title="Workflow Options"
            variant="link"
            aria-label="Workflow Options"
            class="editor-button-options"
            v-b-tooltip.hover
        >
            <template v-slot:button-content>
                <span class="fa fa-cog" />
            </template>
            <b-dropdown-item href="#" @click="$emit('onSaveAs')"
                ><span class="fa fa-floppy-o mr-1" />Save As...</b-dropdown-item
            >
            <b-dropdown-item href="#" @click="$emit('onLint')"
                ><span class="fa fa-magic mr-1" />Best Practices</b-dropdown-item
            >
            <b-dropdown-item href="#" @click="$emit('onLayout')"
                ><span class="fa fa-align-left mr-1" />Auto Layout</b-dropdown-item
            >
            <b-dropdown-item href="#" @click="$emit('onDownload')"
                ><span class="fa fa-download mr-1" />Download</b-dropdown-item
            >
        </b-dropdown>
        <b-button
            id="workflow-run-button"
            role="button"
            title="Run Workflow"
            variant="link"
            aria-label="Run Workflow"
            class="editor-button-run"
            v-b-tooltip.hover
            @click="$emit('onRun')"
        >
            <span class="fa fa-play" />
        </b-button>
    </div>
</template>

<script>
import { BDropdown, BDropdownItem, BButton } from "bootstrap-vue";

export default {
    components: {
        BDropdown,
        BDropdownItem,
        BButton,
    },
    props: {
        hasChanges: {
            type: Boolean,
        },
        requiredReindex: {
            type: Boolean,
        },
    },
};
</script>
