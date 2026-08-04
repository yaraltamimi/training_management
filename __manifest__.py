{
    'name': 'Training Management',
    'version': '18.0.1.0.0',
    'category': 'Education',
    'summary': 'Manage training and courses',
    'description': 'A module for managing summer training applications and courses.',
    'depends': ['base', 'mail'],
 'data': [
        'security/ir.model.access.csv',
        'views/summer_training_views.xml',
        'views/summer_training_trainee_views.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}