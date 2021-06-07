{
    'name' : 'OMTB',
    'version' : '1.1',
    'summary': 'Online Movie Ticket Booking',
    'sequence': 1,
    'description': """
    """,
    'category': 'Movies Ticket Reservation',
    'website': '',
    'images': [],
    'depends': ['mail', 'web', 'website', 'board',
                ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',

        'wizard/payment_wizard_views.xml',
        'wizard/booking_date_wizard_views.xml',
        'wizard/update_cost_views.xml',

        'views/report/booking_report.xml',
        'views/cinematheater_views.xml',
        'views/movie_views.xml',
        'views/profile_views.xml',
        'views/show_views.xml',
        'views/booking.xml',
        'views/payment_views.xml',
        'views/client_actions_view.xml',

        'views/dash.xml',
        # 'views/reporting_view.xml',
        'views/menu.xml',

        'data/sequence.xml',
        'data/website_menu.xml',
        'data/category_data.xml',
        'data/booking_email_template.xml',
        'data/user_controller_views.xml',
        'data/movie_server_action_data.xml',
    ],
    'demo': [],

    'qweb': [
        "static/src/xml/movie_dashboard_template.xml",
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}