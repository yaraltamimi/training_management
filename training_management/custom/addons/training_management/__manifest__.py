{
    'name': 'Training Management',
    'version': '18.0.1.0.1',
    'category': 'Education',
    'summary': 'Manage training and courses',
    'description': 'A module for managing summer training applications, years, plans, and trainees.',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/summer_training_trainee_views.xml',
        'views/summer_training_year_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}