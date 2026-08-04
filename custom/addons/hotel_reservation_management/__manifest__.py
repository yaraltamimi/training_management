# -*- coding: utf-8 -*-
{
    'name': "Hotel Reservation Management",
    'summary': "Manage hotel guests, rooms, and reservations",
    'description': """Hotel Reservation Management System""",
    'author': "Yara",
    'version': '18.0',
    'depends': ['base', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/root_menus.xml',
        'views/res_partner_views.xml',
        'views/hotel_room_views.xml',
        'views/hotel_reservation_views.xml',
    ],
    'installable': True,
    'application': True,
}