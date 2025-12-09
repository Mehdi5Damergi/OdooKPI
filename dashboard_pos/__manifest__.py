
{
    'name': "POS Dashboard",
    'version': '19.0.1.0.0',
    'category': 'Point of Sale',
    'summary': """Detailed dashboard view for POS""",
    'description': """Customized POS dashboard view""",
    'author': 'Mehdi Damergi',
    'company': 'Mehdi Damergi',
    'maintainer': 'Mehdi Damergi',
    'website': "https://www.linkedin.com/in/mehdi-damergi/",
    'depends': ['hr', 'point_of_sale', 'web'],
    'data': [
        'views/pos_order_views.xml'
    ],
     'assets': {
        'web.assets_backend': [
            'dashboard_pos/static/src/xml/pos_dashboard.xml',
            'dashboard_pos/static/src/js/pos_dashboard.js',
            'dashboard_pos/static/src/css/pos_dashboard.css',
            'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js'
        ],
    },
    'external_dependencies': {
        'python': ['pandas'],
    },
    'images': ['static/description/banner.png'],
    'license': "AGPL-3",
    'installable': True,
    'application': False,
}