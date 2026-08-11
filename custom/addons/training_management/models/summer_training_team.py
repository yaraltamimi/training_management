from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SummerTrainingTeam(models.Model):
    _name = 'summer.training.team'
    _description = 'Summer Training Team Member'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    partner_id = fields.Many2one('res.partner', string='Contact Profile', required=False, tracking=True, ondelete='restrict')

    name = fields.Char(string='Member Name', required=True, tracking=True)
    member_id = fields.Many2one('res.users', string='Related User')

    role = fields.Selection([
        ('manager', 'Training Manager'),
        ('supervisor', 'Company Supervisor'),
        ('trainer', 'Trainer'),
    ], string='Role', required=True, tracking=True)

    year_id = fields.Many2one('summer.training.year', string='Training Year', required=True, tracking=True)

    phone = fields.Char(string='Phone', related='partner_id.phone', store=True, readonly=False)
    email = fields.Char(string='Email', related='partner_id.email', store=True, readonly=False)
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