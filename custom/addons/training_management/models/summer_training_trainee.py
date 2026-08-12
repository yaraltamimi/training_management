from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SummerTrainingTrainee(models.Model):
    _name = 'summer.training.trainee'
    _description = 'Summer Training Trainee'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Trainee Name', required=True, tracking=True)
    user_id = fields.Many2one('res.users', string='Related User', default=lambda self: self.env.user, tracking=True)
    national_id = fields.Char(string='National ID', tracking=True)
    email = fields.Char(string='Email', tracking=True)
    phone = fields.Char(string='Phone', tracking=True)
    birth_date = fields.Date(string='Birth Date')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], string='Gender', tracking=True)

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

    # تم الحفاظ على الربط بالسنة لضمان استقلالية المتدرب
    year_id = fields.Many2one('summer.training.year', string='Training Year', required=True, tracking=True)
    document_ids = fields.One2many('summer.training.trainee.document', 'trainee_id', string='Documents')

    state = fields.Selection([
        ('registered', 'Registered'),
        ('ongoing', 'Under Training'),
        ('completed', 'Completed'),
        ('withdrawn', 'Withdrawn / Excluded'),
    ], string='Status', default='registered', tracking=True)

    withdrawal_reason = fields.Text(string='Withdrawal Reason')
    withdrawal_date = fields.Date(string='Withdrawal Date')

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

    @api.constrains('state', 'withdrawal_date', 'withdrawal_reason')
    def _check_withdrawal_state(self):
        for record in self:
            if record.state == 'withdrawn':
                if not record.withdrawal_date:
                    raise ValidationError('You must specify a withdrawal date when setting the status to Withdrawn/Excluded.')
                if not record.withdrawal_reason:
                    raise ValidationError('You must specify a withdrawal reason when setting the status to Withdrawn/Excluded.')