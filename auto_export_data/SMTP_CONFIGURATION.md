# SMTP Configuration for Auto Export Data Module

This module uses Odoo's standard email functionality to send export files. To configure it to use Yandex SMTP, follow these steps:

## Yandex SMTP Settings

- SMTP Server: smtp.yandex.com
- Port: 587
- Email: shop.2itelecom@yandex.com
- Password: c9bf7819bb42ccc1b53199795f396ff0
- Encryption: STARTTLS

## Configuration Steps

1. **Go to Odoo Settings**
   - Navigate to Settings → General Settings
   - Scroll down to the "Discuss" section

2. **Configure Outgoing Mail Servers**
   - Click on "Outgoing Mail Servers"
   - Click "Create" to add a new mail server
   - Fill in the following details:
     - Description: Yandex SMTP
     - SMTP Server: smtp.yandex.com
     - SMTP Port: 587
     - Connection Security: STARTTLS
     - Username: shop.2itelecom@yandex.com
     - Password: c9bf7819bb42ccc1b53199795f396ff0
     - From Address: shop.2itelecom@yandex.com
     - Test Recipient: (your test email address)
   - Click "Test Connection" to verify the settings
   - If successful, click "Save"

3. **Set as Default**
   - Make sure the "Active" checkbox is checked
   - If you want this to be the default mail server, check the "Default" checkbox

## Verification

After configuring the SMTP settings:
1. Create or edit an export configuration
2. Make sure to select fields to export
3. Run a test export
4. Check that you receive the email with the Excel attachment

## Troubleshooting

If emails are not being sent:
1. Check that the outgoing mail server is properly configured and active
2. Verify the username and password are correct
3. Check Odoo's logs for any error messages
4. Ensure the "From Address" in the mail template matches your Yandex email