# Mail Sender Module

This Odoo module allows you to send emails using your own SMTP servers.

## Features

- Configure multiple SMTP servers
- Send emails with custom subject and HTML body
- Select recipients for each email
- Track email sending status

## Installation

1. Copy this module folder to your Odoo addons directory
2. Update the Apps list in Odoo
3. Install the "Mail Sender" module

## Configuration

1. Go to "Mail Sender > Configuration > SMTP Configurations"
2. Create your SMTP configurations with:
   - Server hostname
   - Port number
   - Username and password
   - Encryption type (None, STARTTLS, SSL/TLS)

## Usage

1. Go to "Mail Sender > Mail Sender"
2. Create a new email:
   - Enter a name for your email
   - Select an SMTP configuration
   - Enter recipient emails (comma separated)
   - Enter a subject
   - Write your email body (HTML supported)
3. Click "Send Mail" to send your email

## Requirements

- Odoo 19
- Python 3.8+
- Access to SMTP servers

## Troubleshooting

If you encounter issues sending emails:

1. Check your SMTP configuration details
2. Ensure your SMTP server allows connections from your Odoo server
3. Verify your credentials are correct
4. Check firewall settings if applicable