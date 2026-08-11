from odoo import models, fields

class SummerTrainingTraineeDocument(models.Model):
    _name = 'summer.training.trainee.document'
    _description = 'Trainee Document'

    name = fields.Char(string='Document Name', required=True)

    document_type = fields.Selection([
        ('id_copy', 'ID Copy'),
        ('acceptance_letter', 'Acceptance Letter'),
        ('certificate', 'Certificate'),
        ('report', 'Report'),
        ('other', 'Other'),
    ], string='Document Type', required=True, default='other')

    trainee_id = fields.Many2one('summer.training.trainee', string='Trainee', required=True, ondelete='cascade')

    file = fields.Binary(string='File', attachment=True)
    document_file = fields.Binary(string='Document File', related='file', store=True, attachment=True)
    file_name = fields.Char(string='File Name')

    upload_date = fields.Date(string='Upload Date', default=fields.Date.context_today)
    notes = fields.Text(string='Notes')