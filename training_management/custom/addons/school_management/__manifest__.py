{
    "name": "School Management",
    "version": "1.0",
    "license": "LGPL-3",
    "summary": "School Management module for Odoo 18",
    "depends": ['account'],
  'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/school_student_view.xml',
        'views/account_move.xml',  
    ],
    "demo": [
        'demo/demo.xml',
    ],
    "installable": True,
    "application": True,
}