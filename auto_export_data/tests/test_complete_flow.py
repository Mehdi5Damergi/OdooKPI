from odoo.tests.common import TransactionCase
import base64


class TestCompleteFlow(TransactionCase):
    def setUp(self):
        super().setUp()
        # Get the partner model
        self.model = self.env["ir.model"].search(
            [("model", "=", "res.partner")], limit=1
        )
        
        # Create test partners
        self.partner1 = self.env["res.partner"].create(
            {
                "name": "Test Partner 1",
                "email": "test1@example.com",
            }
        )
        self.partner2 = self.env["res.partner"].create(
            {
                "name": "Test Partner 2",
                "email": "test2@example.com",
            }
        )

    def test_complete_export_flow(self):
        """Test the complete flow from configuration to email sending"""
        # Create export configuration
        config = self.env["auto.export.config"].create(
            {
                "name": "Complete Flow Test",
                "model_id": self.model.id,
                "domain_filter": "[('id', 'in', [%d, %d])]" % (self.partner1.id, self.partner2.id),
                "email_to": "recipient@example.com",
                "interval_type": "daily",
            }
        )
        
        # Add fields to export
        field_names = ["name", "email"]
        for field_name in field_names:
            self.env["auto.export.config.field"].create(
                {
                    "config_id": config.id,
                    "field_path": field_name,
                    "field_label": field_name.capitalize(),
                }
            )
        
        # Verify fields were added
        self.assertEqual(len(config.field_line_ids), 2, "Should have 2 fields configured")
        
        # Perform export
        config._export_and_send()
        
        # Check that an attachment was created
        attachment = self.env["ir.attachment"].search(
            [
                ("res_model", "=", "auto.export.config"),
                ("res_id", "=", config.id),
            ],
            limit=1,
        )
        self.assertTrue(attachment, "Attachment should be created")
        
        # Check that the attachment has data
        self.assertGreater(len(attachment.datas), 0, "Attachment should contain data")
        
        # Check filename
        self.assertIn(".xlsx", attachment.name, "Attachment should be an Excel file")
        self.assertIn(config.name.replace(" ", "_"), attachment.name, "Filename should include config name")
        
        # Check that cron job can be created
        config._create_or_update_cron()
        self.assertTrue(config.cron_id, "Cron job should be created")
        
        # Check cron properties
        self.assertEqual(config.cron_id.interval_type, "days")
        self.assertEqual(config.cron_id.interval_number, 1)
        self.assertTrue(config.cron_id.active)