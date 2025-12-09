# -*- coding: utf-8 -*-

from odoo.tests.common import TransactionCase


class TestMailSender(TransactionCase):

    def setUp(self):
        super(TestMailSender, self).setUp()
        # Create a test SMTP configuration
        self.smtp_config = self.env['mail.sender.smtp'].create({
            'name': 'Test SMTP',
            'host': 'smtp.example.com',
            'port': 587,
            'username': 'test@example.com',
            'password': 'testpassword',
            'encryption': 'starttls',
            'active': True,
        })

    def test_mail_sender_creation(self):
        """Test creation of mail sender record"""
        mail_sender = self.env['mail.sender'].create({
            'name': 'Test Email',
            'recipient_emails': 'recipient@example.com',
            'subject': 'Test Subject',
            'body': '<p>Test Body</p>',
            'smtp_config_id': self.smtp_config.id,
        })
        
        self.assertEqual(mail_sender.name, 'Test Email')
        self.assertEqual(mail_sender.state, 'draft')