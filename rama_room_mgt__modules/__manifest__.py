# -*- coding: utf-8 -*-
{
    'name': "Room Management - Rama",

    'summary': "Room Management for Task 3",

    'description': """
    This module provides room management functionalities for Task 3
    It includes features for managing rooms, buildings, floors, room types, and amenities.
    """,

    'author': "Muhammad Rama Nurimani",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        'security/room_security.xml',
        'security/ir.model.access.csv',
        'data/sequence_data.xml',
        'views/room_views.xml',
        'views/building_views.xml',
        'views/building_floor_views.xml',
        'views/room_type_views.xml',
        'views/room_amenities_views.xml',
        'views/res_user_views.xml',
        'views/room_reservation_views.xml',
        'views/menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

