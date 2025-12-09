
{
    'name': "Advanced Dynamic Dashboard Odoo19",
    'version': '19.0.1.0.0',
    'category': 'Productivity',
    'summary': """Odoo Dynamic Dashboard, Dynamic Dashboard, Odoo AI, Odoo18, Odoo18 Dashboards, Dashboard with AI, AI Dashboard, Odoo Dashboard,Graph View,""",
    'description': """Create Configurable Odoo Dynamic Dashboard to get the 
    information that are relevant to your business, department, or a specific 
    process or need""",
    
    'author': 'Mehdi Damergi',
    'company': 'Mehdi Damergi',
    'maintainer': 'Mehdi Damergi',
    'website': "https://www.linkedin.com/in/mehdi-damergi",
    'depends': ['web'],
    'data': [
        'security/ir.model.access.csv',
        'data/dashboard_theme_data.xml',
        'views/dashboard_views.xml',
        'views/dynamic_block_views.xml',
        'views/dashboard_menu_views.xml',
        'views/dashboard_theme_views.xml',
        'wizard/dashboard_mail_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'https://cdnjs.cloudflare.com/ajax/libs/jquery/3.7.1/jquery.min.js',
            'odoo_dynamic_dashboard/static/src/css/**/*.css',
            'odoo_dynamic_dashboard/static/src/scss/**/*.scss',
            'odoo_dynamic_dashboard/static/src/js/**/*.js',
            'odoo_dynamic_dashboard/static/src/xml/**/*.xml',
            'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css',
            'odoo_dynamic_dashboard/static/src/js/interact_min.js'
        ],
    },
    'images': ['static/description/banner.jpg'],
    'license': "AGPL-3",
    'installable': True,
    'auto_install': False,
    'application': True,
}



