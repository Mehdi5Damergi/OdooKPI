from odoo.tests.common import TransactionCase


class TestYandexSMTP(TransactionCase):
    """Test Yandex SMTP configuration and functionality"""

    def setUp(self):
        super().setUp()
        # Create a test export configuration
        self.export_config = self.env['auto.export.config'].create({
            'name': 'Test Export',
            'model_id': self.env.ref('base.model_res_partner').id,
            'interval_type': 'daily',
            'email_to': 'test@example.com',
        })

    def test_smtp_server_creation(self):
        """Test that Yandex SMTP server is created correctly"""
        smtp_server = self.env['ir.mail_server'].search([('name', '=', 'Yandex SMTP')])
        self.assertTrue(smtp_server, "Yandex SMTP server should be created")
        self.assertEqual(smtp_server.smtp_host, 'smtp.yandex.com')
        self.assertEqual(smtp_server.smtp_port, 587)
        self.assertEqual(smtp_server.smtp_user, 'shop.2itelecom@yandex.com')
        self.assertEqual(smtp_server.smtp_encryption, 'starttls')

    def test_smtp_test_method_exists(self):
        """Test that the SMTP test method exists"""
        self.assertTrue(hasattr(self.export_config, 'test_smtp_connection'))