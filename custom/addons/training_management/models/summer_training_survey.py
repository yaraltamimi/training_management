from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SummerTrainingSurvey(models.Model):

    _name = 'summer.training.survey'

    _description = 'Summer Training Survey'

    _inherit = ['mail.thread']



    year_id = fields.Many2one('summer.training.year', string='Training Year', required=True, tracking=True)

    trainee_id = fields.Many2one('summer.training.trainee', string='Trainee', required=True, tracking=True)



    submission_date = fields.Date(

        string='Submission Date', default=fields.Date.context_today

    )


    content_rating = fields.Selection([

        ('1', 'Poor'),

        ('2', 'Fair'),

        ('3', 'Good'),

        ('4', 'Very Good'),

        ('5', 'Excellent'),

    ], string='Content Rating', required=True)


    trainer_rating = fields.Selection([

        ('1', 'Poor'),

        ('2', 'Fair'),

        ('3', 'Good'),

        ('4', 'Very Good'),

        ('5', 'Excellent'),

    ], string='Trainer Rating', required=True)


    organization_rating = fields.Selection([

        ('1', 'Poor'),

        ('2', 'Fair'),

        ('3', 'Good'),

        ('4', 'Very Good'),

        ('5', 'Excellent'),

    ], string='Organization Rating', required=True)


    overall_satisfaction = fields.Selection([

        ('1', 'Poor'),

        ('2', 'Fair'),

        ('3', 'Good'),

        ('4', 'Very Good'),

        ('5', 'Excellent'),

    ], string='Overall Satisfaction', required=True)


    comments = fields.Text(string='Additional Comments')



    _sql_constraints = [

        ('unique_survey_per_trainee_year', 'unique(trainee_id, year_id)',

         'This trainee has already submitted a survey for this training year!'),

    ]



    @api.constrains('trainee_id', 'year_id')

    def _check_trainee_year_match(self):

        for record in self:

            if not record.trainee_id or not record.year_id:

                continue

            if record.trainee_id.year_id != record.year_id:

                raise ValidationError(

                    'The selected trainee does not belong to the selected training year.'

                )