from odoo import api, fields, models, _
import io
import xlsxwriter
import base64
from datetime import datetime


class ExcelExport(models.TransientModel):
    _name = 'excelexport'
    _description = "Export query result to Excel"

    def get_default_caution_html(self):
        return _("""
        <div>
            <span style='color: red'>Be careful</span>, it will execute the query <span style='color: red; text-decoration: underline'>one more time</span> on your database in order to get-back the datas used to export the result.
            <br/>
            For example, query with <span style='color: orange'>CREATE</span> or <span style='color: orange'>UPDATE</span> statement without any 'RETURNING' statement will not necessary export a table unlike <span style='color: blue'>SELECT</span> statement,
            <br/>
            <span style='text-decoration: underline'>but it will still be executed one time in the background during the attempt of exporting process</span>.
            <br/>
            So when you want to export the result, use preferably 'SELECT' statement to be sure to not execute an unwanted query twice.
        </div>
        """)

    name = fields.Text(string="Query")
    query_id = fields.Many2one('querydeluxe', string="Query origin")
    caution_html = fields.Html(string="CAUTION", default=get_default_caution_html)
    understand = fields.Boolean(string="I understand")

    def export_excel(self):
        if self:
            self = self.sudo()
            first = self[0]
            
            # Get the query result
            headers, datas = first.query_id._get_result_from_query(first.query_id.name)
            
            # Create an in-memory output file for the new workbook.
            output = io.BytesIO()

            # Even though the final file will be in memory the module uses temp
            # files during assembly for efficiency. To avoid this on servers
            # that don't allow temp files, for example the Google APP Engine,
            # set the 'in_memory' Workbook() constructor option as shown
            # in the docs.
            workbook = xlsxwriter.Workbook(output, {'in_memory': True})
            worksheet = workbook.add_worksheet()

            # Write headers
            header_format = workbook.add_format({
                'bold': True,
                'bg_color': '#D3D3D3',
                'border': 1
            })
            
            if headers:
                for col_num, header in enumerate(headers):
                    worksheet.write(0, col_num + 1, str(header), header_format)
                
                # Write row numbers
                row_number_format = workbook.add_format({
                    'bold': True,
                    'bg_color': 'yellow',
                    'border': 1
                })
                
                for row_num in range(len(datas)):
                    worksheet.write(row_num + 1, 0, row_num + 1, row_number_format)

                # Write data
                for row_num, row_data in enumerate(datas):
                    for col_num, cell_data in enumerate(row_data):
                        worksheet.write(row_num + 1, col_num + 1, str(cell_data) if cell_data is not None else '')

            workbook.close()

            # Rewind the buffer.
            output.seek(0)

            # Set the filename
            filename = f"query_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

            # Create the attachment
            attachment = self.env['ir.attachment'].create({
                'name': filename,
                'type': 'binary',
                'datas': base64.b64encode(output.read()),
                'store_fname': filename,
                'res_model': 'querydeluxe',
                'res_id': first.query_id.id,
                'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            })

            # Close the BytesIO object
            output.close()

            # Return the URL to download the attachment
            return {
                'type': 'ir.actions.act_url',
                'url': '/web/content/%s?download=true' % attachment.id,
                'target': 'self',
            }