{
    'name' : 'OLMS',
    'version' : '1.1',
    'summary': 'Online Library Management',
    'sequence': 1,
    'description': """
    """,
    'category': 'Online Library Management System',
    'website': '',
    'images': [],
    'depends': [ 'mail', 'web', 'website','purchase',
            ],
    'data': [
            'security/library_security.xml',
            'security/ir.model.access.csv',

            'data/master_data.xml',
            'data/controller_views.xml',
            'data/sequence.xml',
            'data/website_menu.xml',
            'data/send_email_template.xml',
            'data/server_action_data.xml',

            'wizard/update_book.xml',
            'wizard/date_wizard_views.xml',
            'wizard/payment_wizard_views.xml',

            'views/report/report.xml',
            'views/client_actions_view.xml',
            'views/profile.xml',
            'views/library.xml',
            'views/book.xml',
            'views/payment_views.xml',
            'views/menu.xml',

    ],
    'demo': [],

    'qweb': [
            "static/src/xml/dashboard_template.xml",
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}