from odoo import models, fields

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