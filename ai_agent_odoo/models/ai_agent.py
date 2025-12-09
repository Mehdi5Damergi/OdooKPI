# -*- coding: utf-8 -*-
from odoo import models, fields, api


class AIAgent(models.Model):
    _name = 'ai.agent'
    _description = 'AI Assistant Configuration'
    
    # Configuration fields
    name = fields.Char(string='Name', required=True, default='AI Assistant')
    active = fields.Boolean(string='Active', default=True)
    
    # API Configuration
    service_url = fields.Char(string='Service URL', default='https://openrouter.ai/api/v1/chat/completions')
    api_key = fields.Char(string='API Key')
    
    @api.model
    def get_ai_config(self):
        """Get AI configuration from system parameters or model fields"""
        config_param = self.env['ir.config_parameter']
        
        service_url = config_param.sudo().get_param(
            'ai_agent_odoo.service_url', 
            self.service_url
        )
        api_key = config_param.sudo().get_param(
            'ai_agent_odoo.api_key', 
            self.api_key or ''
        )
        
        return {
            'service_url': service_url,
            'api_key': api_key
        }
    
    @api.model
    def get_partner_data(self, limit=10, domain=None):
        """Get partner data for AI context"""
        if domain is None:
            domain = []
            
        partners = self.env['res.partner'].sudo().search(domain, limit=limit)
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
        
        return partner_data
    
    @api.model
    def get_product_data(self, limit=10, domain=None):
        """Get product data for AI context"""
        if domain is None:
            domain = []
            
        products = self.env['product.product'].sudo().search(domain, limit=limit)
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
        
        return product_data
    
    @api.model
    def get_sale_order_data(self, limit=10, domain=None):
        """Get sale order data for AI context"""
        if domain is None:
            domain = []
            
        orders = self.env['sale.order'].sudo().search(domain, limit=limit)
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
        
        return order_data