/** @odoo-module **/

import {registry} from "@web/core/registry";
import {useService} from "@web/core/utils/hooks";
import {Component} from "@odoo/owl";
import {rpc} from "@web/core/network/rpc";
import {xml} from "@odoo/owl";
import {CustomExportDataDialog} from "@auto_export_data/js/export_data_custom_dialog";
import {patch} from "@web/core/utils/patch";

const actionRegistry = registry.category("actions");

export class FieldPickerDialogClientAction extends Component {
    static template = xml`<div class="field_picker_client_action"></div>`;
    static props = ["*"];

    setup() {
        console.log("FieldPickerDialogClientAction setup called");
        this.dialogService = useService("dialog");
        this.showDialog();
    }

    async showDialog() {
        console.log("showDialog called with props:", this.props);
        const {model, config_id} = this.props.action.params;

        await this.dialogService.add(CustomExportDataDialog, {
            root: {resModel: model},
            defaultExportList: [],
            getExportedFields: async (modelName, isCompatible, parentParams) => {
                // Use our own method to get model fields
                const result = await rpc("/auto_export_data/get_model_fields", {
                    model: modelName,
                    config_id: config_id,
                });
                return result;
            },
            download: async (fields, isCompatible, format) => {
                const selectedFields = fields.map((f) => f.id);
                console.log("Saving fields:", selectedFields);
                await rpc("/auto_export_data/save_field_picker", {
                    config_id,
                    field_paths: selectedFields,
                });
                this.env.services.notification.add("Fields saved to export config!", {
                    type: "success",
                });
                this.dialogService.closeAll();
                this.env.services.action.restore();
            },
            close: () => {
                this.dialogService.closeAll();
            },
        });
    }
}

actionRegistry.add("open_field_picker_dialog", FieldPickerDialogClientAction, {
    force: true,
});
