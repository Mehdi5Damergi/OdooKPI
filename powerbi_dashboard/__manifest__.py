{
    'name': 'Power BI Dashboard',
    'version': '19.0.1.0.0',
    'category': 'Extra Tools',
    'summary': 'Affiche un tableau de bord Power BI intégré dans Odoo.',
    'description': """
Module Odoo pour intégrer un tableau de bord Power BI via un iframe.
    """,
    'author': 'Mehdi Damergi',
    'website': 'https://www.linkedin.com/in/mehdi-damergi',
    'depends': ['base', 'web'],
    'data': [
        'views/powerbi_dashboard_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'powerbi_dashboard/static/src/powerbi_dashboard.js',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}