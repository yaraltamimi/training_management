from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SummerTrainingPlan(models.Model):
    _name = 'summer.training.plan'
    _description = 'Summer Training Plan & Weeks'
    _order = 'sequence, id'

    sequence = fields.Integer(string='Sequence', default=10)
    name = fields.Char(string='Week / Topic Title', required=True)
    
    activity_type = fields.Selection([
        ('practical', 'Practical Task'),
        ('theoretical', 'Theoretical / Lecture'),
        ('project', 'Project Deliverable'),
        ('exam', 'Assessment / Exam')
    ], string='Activity Type', default='practical')
    
    supervisor_feedback = fields.Text(string="Supervisor's Notes & Feedback")
    
    is_completed = fields.Boolean(string='Completed', default=False)
    
    year_id = fields.Many2one('summer.training.year', string='Training Year', ondelete='cascade')
    
    day_ids = fields.One2many('summer.training.day', 'plan_id', string='Daily Schedule')

    @api.constrains('day_ids')
    def _check_days_count(self):
        for record in self:
            if len(record.day_ids) > 5:
                raise ValidationError("Sorry, the maximum limit is 5 days per week!")


class SummerTrainingDay(models.Model):
    _name = 'summer.training.day'
    _description = 'Summer Training Day Plan'
    _order = 'id'

    name = fields.Char(string='Day Title / Topic', required=True)
    day_of_week = fields.Selection([
        ('sunday', 'Sunday'),
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
    ], string='Day', required=True)
    description = fields.Text(string='Daily Tasks & Schedule')
    plan_id = fields.Many2one(
        'summer.training.plan', 
        string='Training Plan', 
        ondelete='cascade', 
        required=True,
        default=lambda self: self.env.context.get('default_plan_id') or self.env.context.get('active_id')
    )