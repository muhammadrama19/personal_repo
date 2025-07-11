# -*- coding: utf-8 -*-
{
    'name': "Transportation Management Rama",

    'summary': "Transportation Management System Bus and Passenger",

    'description': """
Transportation Management System
    """,

    'author': "Muhammad Rama Nurimani",
    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base', 'hr','mail'],

    'data': [
        'security/transportation_security.xml',
        'security/ir.model.access.csv',
        'data/sequence_data.xml',
        'data/bus_data.xml',
        'data/passenger_data.xml',
        'data/routes_data.xml',
        'data/schedule_data.xml',
        'views/driver_views.xml',
        'views/routes_views.xml',
        'views/bus_views.xml',
        'views/schedule_views.xml',
        'views/passenger_views.xml',
        'views/baggage_views.xml',
        'views/menu.xml'
    ],
 
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True
}


