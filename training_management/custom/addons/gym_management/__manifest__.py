{
    'name': 'Gym Management',
    'version': '1.0',
    'summary': 'Manage gym members and subscriptions',
    'category': 'Services',
    'author': 'Yara',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/gym_member_views.xml',
    ],
    'installable': True,
    'application': True,
}