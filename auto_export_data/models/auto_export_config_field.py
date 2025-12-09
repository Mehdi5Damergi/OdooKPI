from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval


class AutoExportConfigField(models.Model):
    _name = "auto.export.config.field"
    _description = "Export Field Line"
    _order = "sequence, id"

    config_id = fields.Many2one(
        "auto.export.config",
        required=True,
        ondelete="cascade",
    )
    field_path = fields.Char(
        string="Field Path",
        required=True,
        help="Use dot notation for sub-fields, e.g. partner_id.email",
    )
    field_label = fields.Char(string="Label", required=True)
    sequence = fields.Integer(default=1)
