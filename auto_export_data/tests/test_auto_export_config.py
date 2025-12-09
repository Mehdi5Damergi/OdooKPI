from odoo.tests.common import TransactionCase


class TestAutoExportConfig(TransactionCase):
    def setUp(self):
        super().setUp()
        self.model = self.env["ir.model"].search(
            [("model", "=", "res.partner")], limit=1
        )
        self.partner = self.env["res.partner"].create(
            {
                "name": "Test Partner",
                "email": "test@example.com",
            }
        )
        self.config = self.env["auto.export.config"].create(
            {
                "name": "Test Export",
                "model_id": self.model.id,
                "domain_filter": "[('id', '=', %d)]" % self.partner.id,
                "email_to": "recipient@example.com",
                "interval_type": "daily",
            }
        )
        self.field_line = self.env["auto.export.config.field"].create(
            {
                "config_id": self.config.id,
                "field_path": "name",
                "field_label": "Partner Name",
            }
        )

    def test_onchange_model_unlinks_fields(self):
        self.assertTrue(self.config.field_line_ids)
        self.config.onchange_model_()
        self.assertFalse(self.config.field_line_ids)

    def test_save_field_picker_selection(self):
        self.config.save_field_picker_selection(self.config.id, ["name", "email"])
        self.assertEqual(len(self.config.field_line_ids), 2)
        self.assertEqual(self.config.field_line_ids[0].field_path, "name")
        self.assertEqual(self.config.field_line_ids[1].field_path, "email")

    def test_get_model_fields_for_picker(self):
        fields = self.config.get_model_fields_for_picker(self.config.id)
        self.assertTrue(any(f["name"] == "name" for f in fields))
        self.assertTrue(any(f["name"] == "email" for f in fields))

    def test_get_field_value(self):
        value = self.config._get_field_value(self.partner, "name")
        self.assertEqual(value, "Test Partner")

    def test_get_field_values_for_export(self):
        values = self.config._get_field_values_for_export(self.partner, "name")
        self.assertEqual(values, ["Test Partner"])

    def test_export_and_send_creates_attachment_and_mail(self):
        # Add a second field for export
        self.env["auto.export.config.field"].create(
            {
                "config_id": self.config.id,
                "field_path": "email",
                "field_label": "Email",
            }
        )
        # Should not raise
        self.config._export_and_send()
        # Check attachment
        attachment = self.env["ir.attachment"].search(
            [
                ("res_model", "=", "auto.export.config"),
                ("res_id", "=", self.config.id),
            ],
            limit=1,
        )
        self.assertTrue(attachment)
        # Check mail
        mail = self.env["mail.mail"].search(
            [
                ("email_to", "=", "recipient@example.com"),
                ("subject", "ilike", "Auto Export"),
            ],
            limit=1,
        )
        self.assertTrue(mail)
