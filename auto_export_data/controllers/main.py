from odoo import http
from odoo.http import request, route


class ExportAutoDataController(http.Controller):
    @route("/auto_export_data/save_field_picker", type="json", auth="user")
    def save_field_picker(self, config_id, field_paths):
        request.env["auto.export.config"].save_field_picker_selection(
            config_id, field_paths
        )
        return {"status": "ok"}

    @route("/auto_export_data/get_model_fields", type="json", auth="user")
    def get_model_fields(self, model, config_id):
        try:
            # Get fields for the model using our own method
            fields_data = request.env["auto.export.config"].get_model_fields_for_picker(
                int(config_id)
            )
            
            # Convert to the format expected by the export dialog
            result = []
            if fields_data:  # Ensure fields_data is not None or empty
                for field in fields_data:
                    result.append({
                        'id': field['name'],
                        'name': field['string'],
                        'type': field['type'],
                        'relation': field['relation'] or '',
                        'value': field['name'],
                        'children': field['type'] in ['one2many', 'many2many', 'many2one'],
                        'field': field['name'],
                        'required': False,
                        'readonly': False,
                        'help': '',
                        'string': field['string']
                    })
            
            return result
        except Exception as e:
            # Return empty array in case of error
            return []
