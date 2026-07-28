from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SummerTrainingYear(models.Model):
    _name = 'summer.training.year'
    _description = 'Summer Training Year'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Year Name', required=True)
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    
    weeks_count = fields.Integer(string='Number of Weeks', compute='_compute_weeks', store=True)
    
    plan_ids = fields.One2many('summer.training.plan', 'year_id', string='Training Plans & Weeks')
    document_ids = fields.One2many('summer.training.year.document', 'training_year_id', string='Documents')
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('planned', 'Planned'),
        ('ongoing', 'Ongoing'),
        ('done', 'Done'),
        ('archived', 'Archived')
    ], string='Status', default='draft', tracking=True)

    @api.depends('start_date', 'end_date')
    def _compute_weeks(self):
        for record in self:
            if record.start_date and record.end_date:
                if record.end_date < record.start_date:
                    record.weeks_count = 0
                else:
                    delta = record.end_date - record.start_date
                    days = delta.days + 1
                    record.weeks_count = max(1, round(days / 7))
            else:
                record.weeks_count = 0

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for record in self:
            if record.start_date and record.end_date and record.end_date < record.start_date:
                raise ValidationError("End Date cannot be earlier than Start Date!")

    def action_planned(self):
        for record in self:
            record.state = 'planned'

    def action_ongoing(self):
        for record in self:
            record.state = 'ongoing'

    def action_done(self):
        for record in self:
            record.state = 'done'

    def action_archived(self):
        for record in self:
            record.state = 'archived'