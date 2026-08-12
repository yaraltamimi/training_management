from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SummerTrainingSurvey(models.Model):
    _name = 'summer.training.survey'
    _description = 'Summer Training Survey'
    _inherit = ['mail.thread']

    survey_type = fields.Selection([
        ('trainee', 'Trainee Evaluation'),
        ('year', 'Training Year Evaluation'),
    ], string='Evaluation Type', default='trainee', required=True, tracking=True)

    year_id = fields.Many2one('summer.training.year', string='Training Year', required=True, tracking=True)
    trainee_id = fields.Many2one('summer.training.trainee', string='Trainee', tracking=True)

    submission_date = fields.Date(
        string='Submission Date', default=fields.Date.context_today
    )

    attendance_rating = fields.Selection([
        ('1', 'Poor'),
        ('2', 'Fair'),
        ('3', 'Good'),
        ('4', 'Very Good'),
        ('5', 'Excellent'),
    ], string='Attendance Rating')

    performance_rating = fields.Selection([
        ('1', 'Poor'),
        ('2', 'Fair'),
        ('3', 'Good'),
        ('4', 'Very Good'),
        ('5', 'Excellent'),
    ], string='Performance Rating')

    commitment_rating = fields.Selection([
        ('1', 'Poor'),
        ('2', 'Fair'),
        ('3', 'Good'),
        ('4', 'Very Good'),
        ('5', 'Excellent'),
    ], string='Commitment Rating')

    content_rating = fields.Selection([
        ('1', 'Poor'),
        ('2', 'Fair'),
        ('3', 'Good'),
        ('4', 'Very Good'),
        ('5', 'Excellent'),
    ], string='Content Rating')

    trainer_rating = fields.Selection([
        ('1', 'Poor'),
        ('2', 'Fair'),
        ('3', 'Good'),
        ('4', 'Very Good'),
        ('5', 'Excellent'),
    ], string='Trainer Rating')

    organization_rating = fields.Selection([
        ('1', 'Poor'),
        ('2', 'Fair'),
        ('3', 'Good'),
        ('4', 'Very Good'),
        ('5', 'Excellent'),
    ], string='Organization Rating')

    overall_satisfaction = fields.Selection([
        ('1', 'Poor'),
        ('2', 'Fair'),
        ('3', 'Good'),
        ('4', 'Very Good'),
        ('5', 'Excellent'),
    ], string='Overall Satisfaction')

    comments = fields.Text(string='Additional Comments')

    @api.constrains('trainee_id', 'year_id', 'survey_type')
    def _check_trainee_year_match(self):
        for record in self:
            if record.survey_type == 'trainee':
                if not record.trainee_id:
                    raise ValidationError('Trainee is required for trainee evaluations.')
                if record.trainee_id and record.year_id and hasattr(record.trainee_id, 'year_id') and record.trainee_id.year_id and record.trainee_id.year_id != record.year_id:
                    raise ValidationError(
                        'The selected trainee does not belong to the selected training year.'
                    )