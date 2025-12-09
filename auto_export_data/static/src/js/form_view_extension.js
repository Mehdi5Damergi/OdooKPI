/** @odoo-module **/

import {FormController} from "@web/views/form/form_controller";
import {patch} from "@web/core/utils/patch";
import {useService} from "@web/core/utils/hooks";
import {rpc} from "@web/core/network/rpc";
//import { ExportDataDialog } from "@web/views/view_dialogs/export_data_dialog";
import {CustomExportDataDialog} from "@auto_export_data/js/export_data_custom_dialog";

patch(FormController.prototype, {
    setup() {
        super.setup();
        this.dialogService = useService("dialog");
        this.notificationService = useService("notification");
    },

    async open_field_picker() {
        console.log("open_field_picker method called!");
        const record = this.model.root;
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
                this.env.services.action.restore();
                // Reload the form to show updated fields
                await this.model.root.load();
            },
            close: () => {
                this.dialogService.closeAll();
            },
        });
    },
});
