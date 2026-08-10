from odoo import models, fields, api
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
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    hours = fields.Float(string='Hours', digits=(16, 0))

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for record in self:
            if record.start_date and record.end_date and record.end_date < record.start_date:
                raise ValidationError("End Date cannot be earlier than Start Date!")


    @api.onchange('year_id')
    def _onchange_year_id(self):
        if self.year_id:
            self.start_date = self.year_id.start_date
            self.end_date = self.year_id.end_date
            self.hours = self.year_id.total_hours                