from odoo import models, fields

class SummerTrainingYear(models.Model):
    _name = 'summer.training.year'
    _description = 'Summer Training Year'

    name = fields.Char(string='Year Name', required=True)
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    weeks_count = fields.Integer(string='Number of Weeks')
    total_hours = fields.Float(string='Total Hours')
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('planned', 'Planned'),
        ('ongoing', 'Ongoing'),
        ('done', 'Done'),
        ('archived', 'Archived')
    ], string='Status', default='draft', tracking=True)