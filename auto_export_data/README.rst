Auto Export to Excel by Schedule
================================

This module allows scheduled export of any model's data to Excel (.xlsx)
and sends it by email automatically using Odoo's standard email functionality.

Features:
---------
- Select fields via a dialog interface
- Define domain filters
- Schedule daily/weekly/monthly export
- Emails the export file using Odoo's standard email system
- Automatic retry mechanism for failed emails
- Detailed logging for troubleshooting

Prerequisites:
--------------
1. Configure Yandex SMTP in Odoo Settings:
   - Go to Settings → General Settings → Discuss
   - Configure Outgoing Mail Servers with:
     - SMTP Server: smtp.yandex.com
     - Port: 587
     - Connection Security: STARTTLS
     - Username: shop.2itelecom@yandex.com
     - Password: c9bf7819bb42ccc1b53199795f396ff0
     - From Address: shop.2itelecom@yandex.com

Usage:
------
1. Go to *Auto Export Configurations*
2. Create a record, select model and fields
3. Configure recipients and schedule
4. Activate the scheduler

Maintainer:
-----------
Synodica Solutions Pvt. Ltd.
