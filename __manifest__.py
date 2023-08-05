{
        'name': 'Hotel Management',
        'version': '16.0.1.0',
        'depends': ['base', 'mail','account'],
        'data': [
                'security/security_groups.xml',
                'security/ir.model.access.csv',
                'views/hotel_management_views.xml',
                'views/hotel_reception_views.xml',
                'data/hotel_accommodation_sequence_number.xml',
                'views/hotel_guest_information_views.xml',
                'views/hotel_order_food_views.xml',
                'views/hotel_food_items_views.xml',
                'views/hotel_menu.xml'
        ],
        'application': True
}
