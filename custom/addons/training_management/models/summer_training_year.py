from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SummerTrainingYear(models.Model):
    _name = 'summer.training.year'
    _description = 'Summer Training Year'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Year Name', required=True)
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    reference = fields.Char(string='Reference Number', copy=False, readonly=True, default='New')
    
    training_type = fields.Selection([
        ('onsite', 'On-site'),
        ('remote', 'Online'),
        ('hybrid', 'Blended')
    ], string='Training Type', default='onsite', tracking=True)

    weeks_count = fields.Integer(string='Number of Weeks', compute='_compute_weeks', store=True)
    hours_per_week = fields.Float(string='Hours per Week', default=0.0)
    total_hours = fields.Float(string='Total Hours', compute='_compute_total_hours', store=True)
    
    plan_ids = fields.One2many('summer.training.plan', 'year_id', string='Training Plans & Weeks')
    document_ids = fields.One2many('summer.training.year.document', 'training_year_id', string='Documents')
    trainee_ids = fields.One2many('summer.training.trainee', 'year_id', string='Trainees')
    team_ids = fields.One2many('summer.training.team', 'year_id', string='Training Team')
    survey_ids = fields.One2many('summer.training.survey', 'year_id', string='Surveys')

    avg_satisfaction = fields.Float(string='Average Satisfaction', compute='_compute_avg_satisfaction', store=True)

    satisfaction_stars = fields.Selection([
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
    ], string='Satisfaction (Stars)', compute='_compute_satisfaction_stars', store=True)
    
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

    @api.depends('weeks_count', 'hours_per_week')
    def _compute_total_hours(self):
        for record in self:
            record.total_hours = record.weeks_count * record.hours_per_week

    @api.depends('survey_ids.overall_satisfaction')
    def _compute_avg_satisfaction(self):
        for record in self:
            ratings = record.survey_ids.mapped('overall_satisfaction')
            if ratings:
                values = [int(r) for r in ratings if r]
                record.avg_satisfaction = sum(values) / len(values)
            else:
                record.avg_satisfaction = 0.0

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('reference', 'New') == 'New':
                vals['reference'] = self.env['ir.sequence'].next_by_code(
                    'summer.training.year'
                ) or 'New'
        return super().create(vals_list)

    @api.depends('avg_satisfaction')
    def _compute_satisfaction_stars(self):
        for record in self:
            stars = round(record.avg_satisfaction) - 1
            record.satisfaction_stars = str(max(0, min(4, stars)))

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for record in self:
            if record.start_date and record.end_date and record.end_date < record.start_date:
                raise ValidationError("End Date cannot be earlier than Start Date!")

            if record.start_date and record.end_date:
                overlapping = self.search([
                    ('id', '!=', record.id),
                    ('start_date', '<=', record.end_date),
                    ('end_date', '>=', record.start_date),
                ])
                if overlapping:
                    raise ValidationError("This training year's dates overlap with an existing training year: %s" % overlapping[0].name)   

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
            