from odoo import models, fields

class SummerTrainingYearDocument(models.Model):
    _name = 'summer.training.year.document'
    _description = 'Summer Training Year Documents & Reports'

    name = fields.Char(string='Document Name', required=True)
    document_file = fields.Binary(string='Upload File', attachment=True, required=True)
    file_name = fields.Char(string='File Name')
    
    document_type = fields.Selection([
        ('plan', 'Approved Plan'),
        ('schedule', 'Schedules'),
        ('report', 'Final Report'),
        ('other', 'Other')
    ], string='Document Type', default='plan', required=True)

    training_year_id = fields.Many2one('summer.training.year', string='Training Year', ondelete='cascade')