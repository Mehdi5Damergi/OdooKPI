# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SMTPConfig(models.Model):
    _name = 'mail.sender.smtp'
    _description = 'SMTP Configuration'

    name = fields.Char(string='Name', required=True)
    host = fields.Char(string='SMTP Host', required=True)
    port = fields.Integer(string='Port', required=True, default=587)
    username = fields.Char(string='Username')
    password = fields.Char(string='Password')
    encryption = fields.Selection([
        ('none', 'No encryption'),
        ('starttls', 'STARTTLS'),
        ('ssl', 'SSL/TLS')
    ], string='Encryption', default='starttls')
    active = fields.Boolean(string='Active', default=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)