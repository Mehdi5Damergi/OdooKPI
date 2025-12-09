# -*- coding: utf-8 -*-
# Copyright 2024 RL Software Development ApS. See LICENSE file for full copyright and licensing details.
{
    'name': "Dashboard for Sale",

    'summary': """
    
    """,

    'description': """
        Contact Mehdi Damergi for more information
    """,

    'author': "Mehdi Damergi",
    'website': "https://www.linkedin.com/in/mehdi-damergi",

    'category': 'Sales/Sales',
    'version': '19.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'web',
        'sale',
        'board',
    ],

    # always loaded
    'data': [        
        'views/menu.xml',        
    ],
    'assets': {
        'web.assets_backend': [
            'dashboard_sale/static/src/components/**/*.xml',
            'dashboard_sale/static/src/components/**/*.js',
            'dashboard_sale/static/src/components/components/**/*.xml',
            'dashboard_sale/static/src/components/components/**/*.js',
        ],
    },
    'demo': [
    
    ], 

    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'OPL-1',
}