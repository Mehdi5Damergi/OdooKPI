from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
import base64


class TestSMTPExport(TransactionCase):
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
        
        # Create export configuration
        self.config = self.env["auto.export.config"].create(
            {
                "name": "Test SMTP Export",
                "model_id": self.model.id,
                "domain_filter": "[]",  # Export all partners
                "email_to": "recipient@example.com",
                "interval_type": "daily",
            }
        )
        
        # Add fields to export
        self.env["auto.export.config.field"].create(
            {
                "config_id": self.config.id,
                "field_path": "name",
                "field_label": "Partner Name",
            }
        )
        self.env["auto.export.config.field"].create(
            {
                "config_id": self.config.id,
                "field_path": "email",
                "field_label": "Email",
            }
        )

    def test_export_creates_excel_file(self):
        """Test that export creates a valid Excel file with data"""
        # Perform export
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
        
        # Check that the attachment has data
        self.assertGreater(len(attachment.datas), 0, "Attachment should contain data")
        
        # Check filename
        self.assertIn(".xlsx", attachment.name, "Attachment should be an Excel file")

    def test_export_sends_email(self):
        """Test that export sends email (this would be tested with a mock SMTP server in real scenarios)"""
        # For now, just test that the method doesn't raise an exception
        try:
            self.config._export_and_send()
            # If we get here, the method completed without error
            success = True
        except Exception as e:
            success = False
            print(f"Export failed with error: {e}")
        
        self.assertTrue(success, "Export should complete without error")

    def test_cron_job_creation(self):
        """Test that cron job is created correctly"""
        # Trigger cron creation
        self.config._create_or_update_cron()
        
        # Check that cron job exists
        self.assertTrue(self.config.cron_id, "Cron job should be created")
        
        # Check cron job properties
        self.assertEqual(self.config.cron_id.name, f"Auto Export: {self.config.name}")
        self.assertEqual(self.config.cron_id.interval_type, "days")
        self.assertEqual(self.config.cron_id.interval_number, 1)
        self.assertTrue(self.config.cron_id.active)