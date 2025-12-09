# -*- coding: utf-8 -*-
{
    "name": "Mail Sender",
    "summary": "Custom Mail Sender with SMTP Configuration",
    "description": """
        Mail Sender Module
        ==================
        This module allows sending emails with custom SMTP configuration.
        Features:
        - Custom SMTP server list
        - Select recipients, subject and body
        - Send emails with configured SMTP
    """,
    "version": "1.0",
    "category": "Mail",
    "author": "Your Name",
    "depends": ["base", "mail"],
    "data": [
        "security/ir.model.access.csv",
        "views/smtp_config_views.xml",
        "views/mail_sender_views.xml",
        "views/assets.xml",
        "demo/demo_data.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}