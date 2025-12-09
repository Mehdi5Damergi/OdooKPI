# Auto Export Data Module Usage Instructions

This document explains how to properly configure and use the Auto Export Data module to ensure it sends emails with Excel attachments at the correct times.

## Prerequisites

1. Configure Yandex SMTP in Odoo:
   - Option A: Go to Settings → General Settings → Discuss
     - Click on "Outgoing Mail Servers"
     - Create a new server with these settings:
       - SMTP Server: smtp.yandex.com
       - Port: 587
       - Connection Security: STARTTLS
       - Username: shop.2itelecom@yandex.com
       - Password: c9bf7819bb42ccc1b53199795f396ff0
       - From Address: shop.2itelecom@yandex.com
   - Option B: Go to Settings → Yandex SMTP Configuration
     - The system will automatically create a Yandex SMTP server with the correct settings
     - You only need to verify and activate it

## Configuration Steps

### 1. Create Export Configuration

1. Go to Settings → Automation → Auto Export
2. Click "Create" to add a new export configuration
3. Fill in the basic information:
   - Name: Give your export a descriptive name
   - Model: Select the Odoo model you want to export data from
   - Recipients: Enter email addresses (comma separated) that should receive the export
   - Interval Type: Choose how often the export should run (Daily, Weekly, Monthly)

### 2. Select Fields to Export

1. Click the "Fields to Export" button
2. A dialog will appear showing all available fields for the selected model
3. Select the fields you want to include in your export by checking the boxes
4. Click "Export to Excel" to save your field selection

### 3. Set Domain Filter (Optional)

1. In the "Domain" tab, you can set filters to export only specific records
2. Leave it empty (`[]`) to export all records
3. Example: `[('active', '=', True)]` to export only active records

### 4. Activate the Scheduler

1. Click the "Activate Scheduler" button to enable automatic exports
2. The next execution time will be shown

## Verification

After configuring the export:

1. Wait for the scheduled time or manually trigger an export by clicking "Fields to Export" and then "Export to Excel"
2. Check that you receive an email with the Excel attachment
3. Verify that the Excel file contains the expected data

## Troubleshooting

### No Email Received

1. Check that the outgoing mail server is properly configured and active
2. Verify the username and password are correct
3. Check Odoo's logs for any error messages
4. Ensure the "From Address" in the mail template matches your Yandex email

### Empty Excel File

1. Make sure you clicked "Fields to Export" and selected at least one field
2. Check your domain filter to ensure it matches records
3. Test with an empty filter `[]` to export all records
4. Ensure you have access rights to the model and records

### Cron Job Not Running

1. Go to Settings → Technical → Automation → Scheduled Actions
2. Find your export cron job and check if it's active
3. Verify the next execution time
4. Check the cron job logs for any errors

## Example Configuration

Here's a sample configuration for exporting customer data:

- Name: "Customer Export"
- Model: "Contact" (res.partner)
- Recipients: "manager@company.com"
- Interval: "Daily"
- Fields to Export: 
  - Name
  - Email
  - Phone
  - Company
- Domain Filter: `[('customer_rank', '>', 0)]` (to export only customers)

After configuring, activate the scheduler and wait for the next scheduled execution.