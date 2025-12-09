# Export Instructions

This document explains how to properly configure and use the Auto Export Data module to ensure your Excel files contain the expected data.

## Steps to Configure Export

1. **Create a New Export Configuration**
   - Go to Settings > Automation > Auto Export
   - Click "Create" to add a new export configuration

2. **Configure Basic Settings**
   - Give your export a name
   - Select the model you want to export data from
   - Enter recipient email addresses (comma separated)
   - Choose the export frequency (Daily, Weekly, or Monthly)

3. **Select Fields to Export**
   - Click the "Fields to Export" button (this is a crucial step!)
   - A dialog will appear showing all available fields for the selected model
   - Select the fields you want to include in your export by checking the boxes
   - Click "Export to Excel" to save your field selection

4. **Set Domain Filter (Optional)**
   - In the "Domain" tab, you can set filters to export only specific records
   - Leave it empty (`[]`) to export all records
   - Example: `[('active', '=', True)]` to export only active records

5. **Configure Email Settings**
   - Make sure Odoo is configured to send emails via SMTP
   - See SMTP_CONFIGURATION.md for details on setting up Yandex SMTP

6. **Activate the Scheduler**
   - Click the "Activate Scheduler" button to enable automatic exports
   - The next execution time will be shown

## Troubleshooting Empty Excel Files

If your exported Excel files are empty, check these common issues:

1. **No Fields Selected**
   - Make sure you clicked "Fields to Export" and selected at least one field
   - Without selected fields, the Excel file will only contain headers

2. **No Matching Records**
   - Check your domain filter to ensure it matches records
   - Test with an empty filter `[]` to export all records

3. **Model Access Issues**
   - Ensure you have access rights to the model and records
   - Verify that records exist in the model

4. **Incorrect Field Paths**
   - If using relational fields, ensure the field paths are correct
   - Example: `partner_id.name` for a related partner's name

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

After configuring, activate the scheduler and wait for the next scheduled execution, or manually trigger an export by clicking the "Fields to Export" button and selecting "Export to Excel".