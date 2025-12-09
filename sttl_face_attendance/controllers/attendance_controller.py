# -*- coding: utf-8 -*-

from odoo import http, _
from odoo.http import request


class HrAttendance(http.Controller):
    @http.route('/employee/images', type="json", auth="public")
    def get_employee_images(self, employee_id=None):
        # Prevent recursion with a simple flag
        if getattr(self, '_processing_request', False):
            return []
        
        try:
            # Set processing flag
            self._processing_request = True
            
            if employee_id:
                # Fixed: Return all employee data instead of returning inside loop
                employees = request.env['hr.employee'].sudo().search([('id', '=', employee_id)])
                employee_data = []
                for employee in employees:
                    employee_data.append({"employee_id": employee.id, "image": employee.image_1920})
                return employee_data
            else:
                employees = request.env['hr.employee'].sudo().search([])
                employee_data = []
                for employee in employees:
                    employee_data.append({"employee_id": employee.id, "image": employee.image_1920})
                return employee_data
        finally:
            # Reset processing flag
            self._processing_request = False