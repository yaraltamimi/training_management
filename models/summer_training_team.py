from odoo import models, fields
from odoo.exceptions import ValidationError

class SummerTrainingTeam(models.Model):

    _name = 'summer.training.team'

    _description = 'Summer Training Team Member'


    name = fields.Char(string='Member Name', required=True)

    member_id = fields.Many2one('res.users', string='Related User')


    role = fields.Selection([
        ('supervisor', 'Supervisor'),
        ('trainer', 'Trainer'),
    ], string='Role', required=True)


    year_id = fields.Many2one('summer.training.year', string='Training Year', required=True)


    phone = fields.Char(string='Phone')

    email = fields.Char(string='Email')
