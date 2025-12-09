/** @odoo-module **/

import {registry} from "@web/core/registry";
import {useService} from "@web/core/utils/hooks";
import {Component} from "@odoo/owl";
import {rpc} from "@web/core/network/rpc";
import {xml} from "@odoo/owl";
import {CustomExportDataDialog} from "@auto_export_data/js/export_data_custom_dialog";

export class FieldPickerButton extends Component {
    static template = xml`
        <button class="btn btn-primary" t-on-click="openFieldPicker">
            <t t-esc="props.string"/>
        </button>
    `;
    static props = {
        string: String,
        record: Object,
    };

    setup() {
        this.dialogService = useService("dialog");
        this.notificationService = useService("notification");
    }

    async openFieldPicker() {
        const record = this.props.record;
        const model = record.resModel;
        const config_id = record.resId;

        console.log("Opening field picker dialog for:", {model, config_id});

        await this.dialogService.add(CustomExportDataDialog, {
            root: {resModel: model},
            defaultExportList: [],
            getExportedFields: async (modelName, isCompatible, parentParams) => {
                return await rpc("/web/export/get_fields", {
                    model: modelName,
                    domain: [],
                    import_compat: isCompatible,
                    ...parentParams,
                });
            },
            download: async (fields, isCompatible, format) => {
                const selectedFields = fields.map((f) => f.id);
                console.log("Saving fields:", selectedFields);
                await rpc("/auto_export_data/save_field_picker", {
                    config_id,
                    field_paths: selectedFields,
                });
                this.notificationService.add("Fields saved to export config!", {
                    type: "success",
                });
                // Close the dialog after saving
                this.dialogService.closeAll();
                // Trigger a reload of the form
                this.env.services.action.restore();
                this.env.services.action.doAction("reload");
            },
            close: () => {
                this.dialogService.closeAll();
                this.env.services.action.restore();
                this.env.services.action.doAction("reload");
            },
        });
    }
}

// Register the component
registry.category("components").add("FieldPickerButton", FieldPickerButton);
