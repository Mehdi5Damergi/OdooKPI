import base64
from datetime import datetime
from io import BytesIO
import logging
import xlsxwriter
from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval
_logger = logging.getLogger(__name__)


class AutoExportConfig(models.Model):
    _name = "auto.export.config"
    _description = "Scheduled Excel Export"
    _inherit = ["mail.thread", "mail.activity.mixin", "utm.mixin"]

    name = fields.Char(string="Export Name", required=True, tracking=True)
    model_id = fields.Many2one(
        "ir.model",
        string="Model",
        required=True,
        ondelete="cascade",
        index=True,
        tracking=True,
    )
    field_line_ids = fields.One2many(
        "auto.export.config.field",
        "config_id",
        string="Fields to Export",
    )
    domain_filter = fields.Char(
        help="Add domain to filter records. Use Odoo domain format.",
        default="[]",
    )
    email_to = fields.Char(
        string="Recipients",
        help="Comma-separated emails",
        tracking=True,
    )
    res_model_name = fields.Char(
        related="model_id.model",
        string="Model Name",
        readonly=True,
        store=True,
    )
    interval_type = fields.Selection(
        [("daily", "Daily"), ("weekly", "Weekly"), ("monthly", "Monthly")],
        default="weekly",
    )
    active = fields.Boolean(default=True, tracking=True)
    cron_id = fields.Many2one(
        "ir.cron",
        string="Scheduled Cron",
        ondelete="set null",
        readonly=True,
        copy=False,
    )
    cron_active = fields.Boolean(default=True, tracking=True)
    cron_nextcall = fields.Datetime(
        related="cron_id.nextcall",
        string="Next Execution",
        store=True,
        readonly=False,
    )
    email_template_id = fields.Many2one(
        "mail.template",
        string="Email Template",
        help="Template for export email",
        default=lambda self: self.env.ref(
            "auto_export_data.mail_template_auto_export_daily", raise_if_not_found=False
        ),
    )

    @api.model
    def create(self, vals):
        rec = super().create(vals)
        rec._create_or_update_cron()
        return rec

    def write(self, vals):
        res = super().write(vals)
        if "interval_type" in vals or "active" in vals:
            self._create_or_update_cron()
        if "active" in vals:
            for rec in self:
                if rec.cron_id:
                    rec.cron_id.active = rec.active
        return res

    def unlink(self):
        for rec in self:
            if rec.cron_id:
                rec.cron_id.unlink()
        return super().unlink()

    def _create_or_update_cron(self):
        for rec in self:
            vals = {
                "name": f"Auto Export: {rec.name}",
                "model_id": self.env.ref(
                    "auto_export_data.model_auto_export_config"
                ).id,
                "state": "code",
                "code": f"model.browse({rec.id})._export_and_send()",
                "user_id": self.env.user.id,
                "active": rec.active,
                "priority": 5,  # Set a priority for the cron job
            }
            if rec.interval_type == "daily":
                vals.update({"interval_type": "days", "interval_number": 1})
            elif rec.interval_type == "weekly":
                vals.update({"interval_type": "weeks", "interval_number": 1})
            elif rec.interval_type == "monthly":
                vals.update({"interval_type": "months", "interval_number": 1})
            if rec.cron_id:
                rec.cron_id.write(vals)
            else:
                cron = self.env["ir.cron"].create(vals)
                rec.cron_id = cron.id

    def action_toggle_cron(self):
        for rec in self:
            if rec.cron_id:
                rec.cron_id.active = not rec.cron_id.active
                rec.cron_active = not rec.cron_id.active

    @api.onchange("interval_type")
    def _onchange_interval_type(self):
        if self.cron_id:
            self._create_or_update_cron()

    def open_field_picker(self):
        """Method called by the button to open the field picker dialog"""
        self.ensure_one()
        return {
            "type": "ir.actions.client",
            "tag": "open_field_picker_dialog",
            "params": {
                "model": self.model_id.model,
                "config_id": self.id,
            },
        }

    @api.model
    def save_field_picker_selection(self, config_id, field_paths):
        config = self.browse(config_id)
        config.field_line_ids.unlink()  # Remove old lines
        # Ensure field_paths is a list
        if not isinstance(field_paths, (list, tuple)):
            field_paths = [field_paths] if field_paths else []
        # Log the field paths being saved
        _logger.info(f"Saving field paths: {field_paths}")
        lines_to_create = []
        for path in field_paths:
            if path:  # Skip empty paths
                # Get a better label for the field
                label = path.split(".")[-1]
                # Try to get the actual field label from the model
                try:
                    model = self.env[config.model_id.model]
                    if "." in path:
                        # Handle sub-fields
                        parts = path.split(".")
                        field_name = parts[0]
                        if field_name in model._fields:
                            field = model._fields[field_name]
                            if hasattr(field, 'string') and field.string:
                                label = field.string + " (" + ".".join(parts[1:]) + ")"
                    else:
                        # Handle direct fields
                        if path in model._fields:
                            field = model._fields[path]
                            if hasattr(field, 'string') and field.string:
                                label = field.string
                except Exception as e:
                    # If we can't get the field label, use the path-based one
                    _logger.warning(f"Could not get field label for {path}: {e}")
                    pass
                lines_to_create.append({
                    "config_id": config.id,
                    "field_path": path,
                    "field_label": label,
                })
        if lines_to_create:
            # Use sudo and specific context to bypass any problematic overrides
            FieldModel = self.env['auto.export.config.field'].sudo().with_context(
                bypass_custom_create=True,
                manual_create=True
            )
            created_fields = []
            for vals in lines_to_create:
                try:
                    field = FieldModel.create(vals)
                    created_fields.append(field)
                except Exception as e:
                    _logger.error(f"Failed to create field {vals.get('field_path')}: {str(e)}")
            _logger.info(f"Successfully created {len(created_fields)} export fields")
        else:
            _logger.warning("No fields to create")
        return True

    @api.model
    def get_model_fields_for_picker(self, config_id, parent_path=None):
        """
        Returns a list of fields for the model (or submodel if parent_path is given),
        with name, string, type, and relation (if relational).
        """
        config = self.browse(config_id)
        model_name = config.model_id.model
        if parent_path:
            # Traverse the parent_path to get the submodel
            attrs = parent_path.split(".")
            model = self.env[model_name]
            for attr in attrs:
                field = model._fields.get(attr)
                if not field:
                    return []
                if field.type in ["many2one", "one2many", "many2many"]:
                    model = self.env[field.comodel_name]
                else:
                    return []
            model_name = model._name
        model = self.env[model_name]
        fields_list = []
        for name, field in model._fields.items():
            field_info = {
                "name": name,
                "string": field.string,
                "type": field.type,
                "relation": field.comodel_name
                if hasattr(field, "comodel_name")
                else False,
            }
            fields_list.append(field_info)
        return fields_list

    def _get_field_value(self, record, field_path):
        """Traverse the field path to get the value,
        supporting relational sub-fields."""
        attrs = field_path.split(".")
        value = record
        for attr in attrs:
            if isinstance(value, models.Model):
                value = getattr(value, attr, False)
            else:
                return ""
            if not value:
                return ""
        # Handle relational types
        if isinstance(value, models.Model):
            return value.display_name
        elif isinstance(value, models.BaseModel):
            return ", ".join(value.mapped("display_name"))
        return str(value)

    def _get_field_values_for_export(self, record, field_path):
        """Traverse the field path, supporting one2many/many2many,
        and return a list of values."""
        try:
            # Handle dot notation as well as slash notation
            if "." in field_path and "/" not in field_path:
                attrs = field_path.split(".")
            else:
                attrs = field_path.split("/")
            value = record
            for i, attr in enumerate(attrs):
                if isinstance(value, models.BaseModel):
                    field = value._fields.get(attr)
                    if not field:
                        return [""]
                    if field.type in ["one2many", "many2many"]:
                        results = []
                        for rec in value[attr]:
                            sub_path = "/".join(attrs[i + 1 :])
                            if sub_path:
                                results.extend(
                                    self._get_field_values_for_export(rec, sub_path)
                                )
                            else:
                                results.append(rec.display_name)
                        return results
                    else:
                        value = value[attr]
                else:
                    return [""]
            if isinstance(value, models.BaseModel):
                return [value.display_name]
            return [str(value) if value is not False else ""]
        except Exception as e:
            _logger.error(f"Error processing field path '{field_path}': {e}")
            return [""]

    def _export_and_send(self):
        self.ensure_one()
        today = datetime.today().date()
        # Check interval_type (cron already handles schedule, but keep for safety)
        if self.interval_type == "weekly":
            pass  # cron handles weekly
        elif self.interval_type == "monthly":
            pass  # cron handles monthly
        # For 'daily', always run
        # Validate that we have a model
        if not self.model_id or not self.model_id.model:
            raise ValueError("No model selected for export")
        model = self.env[self.model_id.model]
        # Validate that we have fields to export
        if not self.field_line_ids:
            raise ValueError("No fields selected for export. Please click 'Fields to Export' and select fields.")
        try:
            domain = safe_eval(self.domain_filter or "[]")
            _logger.info(f"Using domain filter: {self.domain_filter}")
        except Exception as e:
            raise ValueError(f"Invalid domain: {e}") from e
        records = model.search(domain)
        fields_to_export = self.field_line_ids
        # Log information for debugging
        _logger.info(f"Exporting {len(records)} records with {len(fields_to_export)} fields")
        _logger.info(f"Model: {self.model_id.model}")
        _logger.info(f"Field paths: {[f.field_path for f in fields_to_export]}")
        # If no records found, log the total count in the model
        if len(records) == 0:
            total_records = model.search_count([])
            _logger.warning(f"No records found matching domain. Total records in model: {total_records}")
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {"in_memory": True})
        sheet = workbook.add_worksheet()
        # Header row
        for col, field_line in enumerate(fields_to_export):
            sheet.write(0, col, field_line.field_label or field_line.field_path)
        # Data rows (flattened for one2many/many2many)
        rows = []
        # Add a check to ensure we have data to export
        if records and fields_to_export:
            _logger.info(f"Processing {len(records)} records with {len(fields_to_export)} fields")
            for record_idx, record in enumerate(records):
                field_values_lists = []
                max_lines = 1
                for field_line in fields_to_export:
                    try:
                        values = self._get_field_values_for_export(
                            record, field_line.field_path
                        )
                        field_values_lists.append(values)
                        max_lines = max(max_lines, len(values))
                        _logger.debug(f"Field {field_line.field_path} for record {record_idx} has {len(values)} values: {values}")
                    except Exception as e:
                        _logger.error(f"Error getting field values for {field_line.field_path}: {e}")
                        field_values_lists.append([""])
                for i in range(max_lines):
                    row = []
                    for values in field_values_lists:
                        row.append(values[i] if i < len(values) else "")
                    rows.append(row)
            # Write data rows
            for row_idx, row in enumerate(rows, start=1):
                for col_idx, value in enumerate(row):
                    sheet.write(row_idx, col_idx, value)
            _logger.info(f"Successfully processed {len(rows)} data rows")
        else:
            # If no records or fields, still create a file with just headers
            _logger.warning("No records or fields to export")
            # Add a note in the Excel file
            sheet.write(1, 0, "No data to export based on current filters and field selection")
        workbook.close()
        output.seek(0)
        file_data = base64.b64encode(output.read())
        # Clean and join emails for multiple recipients
        recipients = [
            email.strip() for email in (self.email_to or "").split(",") if email.strip()
        ]
        email_to = ",".join(recipients)
        # Format date for filename
        export_date_str = today.strftime("%d_%m_%y")
        attachment = self.env["ir.attachment"].create(
            {
                "name": f"{self.name}_{export_date_str}.xlsx",
                "type": "binary",
                "datas": file_data,
                "res_model": self._name,
                "res_id": self.id,
                "mimetype": (
                    "application/vnd.openxmlformats-officedocument."
                    "spreadsheetml.sheet"
                ),
            }
        )
        # Ensure we have recipients before sending email
        if not email_to:
            _logger.warning("No recipients specified for export email")
            return
        # Use selected email template
        template = self.email_template_id or self.env.ref(
            "auto_export_data.mail_template_auto_export_daily", raise_if_not_found=False
        )
        # Prepare email values
        email_values = {
            "attachment_ids": [(4, attachment.id)], 
            "email_to": email_to,
            "email_from": "shop.2itelecom@yandex.com",
            "auto_delete": True
        }
        try:
            if template:
                # Send email using template
                template.send_mail(self.id, force_send=True, email_values=email_values)
                _logger.info(f"Export email sent successfully using template to {email_to}")
            else:
                # Fallback to direct mail creation
                model_display_name = self.model_id.name or self.model_id.model
                email_body = f"""
                    <p>Dear User,</p>
                    <p>Your scheduled data export <b>{self.name}</b>
                    for the model <b>{model_display_name}
                    </b> has been generated on <b>{export_date_str}</b>.</p>
                    <p>The exported data file is attached to this email.</p>
                    <p>Best regards,<br/>Odoo Automated Export System</p>
                """
                email_values.update(
                    {
                        "subject": f"Auto Export - {self.name}",
                        "body_html": email_body,
                    }
                )
                mail = self.env["mail.mail"].create(email_values)
                mail.send()
                _logger.info(f"Export email sent successfully using fallback method to {email_to}")
        except Exception as e:
            error_msg = f"Failed to send export email to {email_to}: {str(e)}"
            _logger.error(error_msg)
            # Raise a user-friendly error that will appear in the cron logs
            raise Exception(error_msg) from e
