# -*- coding: utf-8 -*-
import logging
import json
from odoo import http
from odoo.http import request
from odoo.tools import ustr

_logger = logging.getLogger(__name__)


class AIAgentController(http.Controller):
    
    @http.route('/ai_agent/config', type='json', auth='user')
    def get_config(self):
        """Return AI service configuration from system parameters"""
        _logger.info("AI Agent config endpoint called")
        
        service_url = request.env['ir.config_parameter'].sudo().get_param(
            'ai_agent_odoo.service_url', 
            'https://openrouter.ai/api/v1/chat/completions'
        )
        api_key = request.env['ir.config_parameter'].sudo().get_param(
            'ai_agent_odoo.api_key', 
            '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'
        )
        
        result = {
            'service_url': service_url,
            'api_key': api_key
        }
        
        _logger.info("AI Agent config endpoint returning: %s", result)
        return result
    
    @http.route('/ai_agent/data/partners', type='json', auth='user')
    def get_partners_data(self, **kwargs):
        """Return partners data for AI context"""
        try:
            limit = kwargs.get('limit', 10)
            domain = kwargs.get('domain', [])
            
            partners = request.env['res.partner'].sudo().search(domain, limit=limit)
            partner_data = []
            
            for partner in partners:
                partner_data.append({
                    'id': partner.id,
                    'name': partner.name,
                    'email': partner.email or '',
                    'phone': partner.phone or '',
                    'company_name': partner.company_name or '',
                    'city': partner.city or '',
                    'country': partner.country_id.name or ''
                })
            
            return {'success': True, 'data': partner_data}
        except Exception as e:
            _logger.error("Error fetching partners data: %s", str(e))
            return {'success': False, 'error': ustr(e)}
    
    @http.route('/ai_agent/data/products', type='json', auth='user')
    def get_products_data(self, **kwargs):
        """Return products data for AI context"""
        try:
            limit = kwargs.get('limit', 10)
            domain = kwargs.get('domain', [])
            
            products = request.env['product.product'].sudo().search(domain, limit=limit)
            product_data = []
            
            for product in products:
                product_data.append({
                    'id': product.id,
                    'name': product.name,
                    'default_code': product.default_code or '',
                    'list_price': product.list_price,
                    'standard_price': product.standard_price,
                    'qty_available': product.qty_available,
                    'uom_name': product.uom_id.name or ''
                })
            
            return {'success': True, 'data': product_data}
        except Exception as e:
            _logger.error("Error fetching products data: %s", str(e))
            return {'success': False, 'error': ustr(e)}
    
    @http.route('/ai_agent/data/sale_orders', type='json', auth='user')
    def get_sale_orders_data(self, **kwargs):
        """Return sale orders data for AI context"""
        try:
            limit = kwargs.get('limit', 10)
            domain = kwargs.get('domain', [])
            
            orders = request.env['sale.order'].sudo().search(domain, limit=limit)
            order_data = []
            
            for order in orders:
                order_data.append({
                    'id': order.id,
                    'name': order.name,
                    'partner_name': order.partner_id.name or '',
                    'date_order': order.date_order.strftime('%Y-%m-%d') if order.date_order else '',
                    'amount_total': order.amount_total,
                    'state': order.state
                })
            
            return {'success': True, 'data': order_data}
        except Exception as e:
            _logger.error("Error fetching sale orders data: %s", str(e))
            return {'success': False, 'error': ustr(e)}