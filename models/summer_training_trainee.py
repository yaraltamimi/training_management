from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SummerTrainingTrainee(models.Model):
    _name = 'summer.training.trainee'
    _description = 'Summer Training Trainee'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # ---- البيانات الشخصية ----
    name = fields.Char(string='Trainee Name', required=True, tracking=True)
    national_id = fields.Char(string='National ID')
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    birth_date = fields.Date(string='Birth Date')
    gender = fields.Selection([
    ('male', 'Male'),
    ('female', 'Female'),
    ], string='Gender')

    # ---- البيانات الأكاديمية ----
    university = fields.Char(string='University / Institution')
    major = fields.Char(string='Major / Specialization')
    academic_level = fields.Selection([
    ('year1', 'First Year'),
    ('year2', 'Second Year'),
    ('year3', 'Third Year'),
    ('year4', 'Fourth Year'),
    ('graduate', 'Graduate'),
    ], string='Academic Level')
    gpa = fields.Float(string='GPA')

    # ---- الربط بالسنة التدريبية ----
    year_id = fields.Many2one('summer.training.year', string='Training Year', required=True, tracking=True)

    state = fields.Selection([
    ('registered', 'Registered'),
    ('ongoing', 'Under Training'),
    ('completed', 'Completed'),
    ('withdrawn', 'Withdrawn / Excluded'),
    ], string='Status', default='registered', tracking=True)

    withdrawal_reason = fields.Text(string='Withdrawal Reason')
    withdrawal_date = fields.Date(string='Withdrawal Date')

    def action_withdraw(self):
        for record in self:
            record.state = 'withdrawn'

    _sql_constraints = [
        ('unique_trainee_per_year', 'unique(national_id, year_id)',
        'This trainee is already registered for this training year!'),
     ]       


    @api.constrains('withdrawal_date', 'year_id')
    def _check_withdrawal_date(self):
        for record in self:
            if not record.withdrawal_date or not record.year_id:
                continue
            if record.year_id.start_date and record.withdrawal_date < record.year_id.start_date:
                raise ValidationError('The withdrawal date cannot be earlier than the start date of the training year.')
            if record.year_id.end_date and record.withdrawal_date > record.year_id.end_date:    
                raise ValidationError('The withdrawal date cannot be later than the end date of the training year.')
           

    @api.constrains('state', 'withdrawal_date')
    def _check_withdrawal_state(self):
         for record in self:
             if record.state == 'withdrawn' and not record.withdrawal_date:
                 raise ValidationError('You must specify a withdrawal date when setting the status to Withdrawn/Excluded.')