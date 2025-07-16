# -*- coding: utf-8 -*-
{
    'name': "NTI Meal Catering",

    'summary': "Meal catering management module, for exam in NTI Odoo Training",

    'description': """
    This modules provides functionalities to manage meal catering services. Which contains weekly meals where each day has a specific meal.
    """,

    'author': "Muhammad Rama Nurimani - Odoo Developer Intern",
    'website': "https://www.yourcompany.com",
    'license': 'LGPL-3',

    'category': 'Meal Catering',
    'version': '0.1',

    'depends': ['base', 'hr', 'purchase', 'product', 'mrp', 'mail'],

    'data': [
        'security/meal_security.xml',
        'security/ir.model.access.csv',
        'security/meal_record_rules.xml',
        'data/meal_sequence.xml',
        'data/meal_lines_sequence.xml',
        'views/meal_order_views.xml',
        'views/meal_schedule_views.xml',
        'views/meal_schedule_line_views.xml',
        'views/meal_menus.xml'
    ],

    'demo': [
        'demo/demo.xml',
    ],
}
