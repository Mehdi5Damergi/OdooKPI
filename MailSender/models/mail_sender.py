# -*- coding: utf-8 -*-

import logging
import base64
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr

_logger = logging.getLogger(__name__)

# Default email template
DEFAULT_EMAIL_TEMPLATE = """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email TunTek</title>
</head>
<body style="margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f4f4f4;">
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #f4f4f4;">
        <tr>
            <td align="center" style="padding: 20px 0;">
                <table width="600" cellpadding="0" cellspacing="0" border="0" style="background-color: #ffffff; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                    
                    <!-- Header -->
                    <tr>
                        <td align="center" style="padding: 30px 20px; background: linear-gradient(135deg, #ff0000 0%, #cc0000 100%); border-radius: 8px 8px 0 0;">
                            <h1 style="color: #ffffff; font-size: 36px; margin: 0; font-weight: bold; letter-spacing: 2px;">
                                TunTek
                            </h1>
                        </td>
                    </tr>
                    
                    <!-- Contenu Principal -->
                    <tr>
                        <td style="padding: 40px 30px;">
                            <h1 style="color: #333333; font-size: 24px; margin: 0 0 20px 0; font-weight: bold;">
                                Bonjour,
                            </h1>
                            
                            <p style="color: #666666; font-size: 16px; line-height: 1.6; margin: 0 0 15px 0;">
                                Nous sommes ravis de vous contacter concernant votre projet.
                            </p>
                            
                            <p style="color: #666666; font-size: 16px; line-height: 1.6; margin: 0 0 15px 0;">
                                Chez <strong style="color: #ff0000;">TunTek</strong>, nous mettons notre expertise à votre service pour vous accompagner dans votre transformation digitale.
                            </p>
                            
                            <p style="color: #666666; font-size: 16px; line-height: 1.6; margin: 0 0 25px 0;">
                                N'hésitez pas à nous contacter pour plus d'informations.
                            </p>
                            
                            <!-- Bouton CTA -->
                            <table width="100%" cellpadding="0" cellspacing="0" border="0">
                                <tr>
                                    <td align="center" style="padding: 10px 0;">
                                        <a href="https://www.2itelecom.com/contactus" style="display: inline-block; padding: 15px 40px; background-color: #ff0000; color: #ffffff; text-decoration: none; border-radius: 5px; font-weight: bold; font-size: 16px;">
                                            Nous Contacter
                                        </a>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                    <!-- Séparateur -->
                    <tr>
                        <td style="padding: 0 30px;">
                            <div style="border-top: 1px solid #eeeeee;"></div>
                        </td>
                    </tr>
                    
                    <!-- Signature -->
                    <tr>
                        <td style="padding: 30px;">
                            <p style="color: #666666; font-size: 14px; line-height: 1.6; margin: 0 0 10px 0;">
                                Cordialement,<br>
                                <strong style="color: #333333;">L'équipe TunTek</strong>
                            </p>
                        </td>
                    </tr>
                    
                    <!-- Footer -->
                    <tr>
                        <td align="center" style="padding: 20px 30px; background-color: #f8f8f8; border-radius: 0 0 8px 8px;">
                            <p style="color: #999999; font-size: 12px; line-height: 1.5; margin: 0 0 10px 0;">
                                <strong style="color: #ff0000;">TunTek</strong> - Solutions Digitales<br>
                                Avenue Dr Mohamed Souissi, Rte Hotel Lido<br>
                                8075 Dar Chaabane el Fehri, Tunisie
                            </p>
                            
                            <p style="color: #999999; font-size: 12px; margin: 10px 0;">
                                📧 <a href="mailto:contact@tuntek.tn" style="color: #ff0000; text-decoration: none;">contact@tuntek.tn</a> | 
                                📱 <a href="tel:+216XXXXXXXX" style="color: #ff0000; text-decoration: none;">+216 XX XXX XXX</a>
                            </p>
                            
                            <!-- Réseaux Sociaux -->
                            <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-top: 15px;">
                                <tr>
                                    <td align="center">
                                        <a href="#" style="display: inline-block; margin: 0 8px;">
                                            <img src="https://img.icons8.com/color/32/000000/linkedin.png" alt="LinkedIn" style="width: 28px; height: 28px;" />
                                        </a>
                                        <a href="#" style="display: inline-block; margin: 0 8px;">
                                            <img src="https://img.icons8.com/color/32/000000/facebook.png" alt="Facebook" style="width: 28px; height: 28px;" />
                                        </a>
                                        <a href="#" style="display: inline-block; margin: 0 8px;">
                                            <img src="https://img.icons8.com/color/32/000000/twitter.png" alt="Twitter" style="width: 28px; height: 28px;" />
                                        </a>
                                    </td>
                                </tr>
                            </table>
                            
                            <p style="color: #cccccc; font-size: 11px; margin: 15px 0 0 0;">
                                © 2025 TunTek. Tous droits réservés.
                            </p>
                        </td>
                    </tr>
                    
                </table>
            </td>
        </tr>
    </table>
</body>
</html>"""


class MailSender(models.Model):
    _name = 'mail.sender'
    _description = 'Mail Sender'

    name = fields.Char(string='Name', required=True)
    recipient_emails = fields.Text(string='Recipient Emails', required=True, 
                                   help='Enter email addresses separated by commas')
    subject = fields.Char(string='Subject', required=True)
    body = fields.Html(string='Body', required=True, default=DEFAULT_EMAIL_TEMPLATE)
    smtp_config_id = fields.Many2one('mail.sender.smtp', string='SMTP Configuration', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('error', 'Error')
    ], string='Status', default='draft')
    
    def action_send_mail(self):
        self.ensure_one()
        try:
            # Parse recipient emails
            recipients = [email.strip() for email in self.recipient_emails.split(',') if email.strip()]
            if not recipients:
                raise ValidationError("Please provide at least one recipient email.")
            
            # Get SMTP configuration
            smtp_config = self.smtp_config_id
            if not smtp_config:
                raise ValidationError("Please select an SMTP configuration.")
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = formataddr((self.env.user.name, smtp_config.username))
            msg['To'] = ', '.join(recipients)
            msg['Subject'] = self.subject
            
            # Attach body
            body = MIMEText(self.body, 'html')
            msg.attach(body)
            
            # Connect to SMTP server
            if smtp_config.encryption == 'ssl':
                server = smtplib.SMTP_SSL(smtp_config.host, smtp_config.port)
            else:
                server = smtplib.SMTP(smtp_config.host, smtp_config.port)
                if smtp_config.encryption == 'starttls':
                    server.starttls()
            
            # Login and send
            if smtp_config.username and smtp_config.password:
                server.login(smtp_config.username, smtp_config.password)
            
            server.send_message(msg)
            server.quit()
            
            # Update state
            self.write({'state': 'sent'})
            
            # Log success
            _logger.info("Email sent successfully to %s", ', '.join(recipients))
            
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Success',
                    'message': 'Email sent successfully!',
                    'type': 'success',
                    'sticky': False
                }
            }
        except Exception as e:
            self.write({'state': 'error'})
            _logger.error("Failed to send email: %s", str(e))
            raise ValidationError("Failed to send email: %s" % str(e))
