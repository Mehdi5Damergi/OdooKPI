from odoo.tests.common import TransactionCase


class TestExportFix(TransactionCase):
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

    def test_export_with_empty_fields_should_raise_error(self):
        """Test that exporting with no fields raises an appropriate error"""
        with self.assertRaises(ValueError) as cm:
            self.config._export_and_send()
        self.assertIn("No fields selected for export", str(cm.exception))

    def test_export_with_valid_fields_should_work(self):
        """Test that exporting with valid fields works correctly"""
        # Add fields for export
        self.env["auto.export.config.field"].create(
            {
                "config_id": self.config.id,
                "field_path": "name",
                "field_label": "Partner Name",
            }
        )
        
        # This should not raise an exception
        try:
            self.config._export_and_send()
            # Check that an attachment was created
            attachment = self.env["ir.attachment"].search(
                [
                    ("res_model", "=", "auto.export.config"),
                    ("res_id", "=", self.config.id),
                ],
                limit=1,
            )
            self.assertTrue(attachment, "Attachment should be created")
        except Exception as e:
            self.fail(f"Export should not raise an exception: {e}")