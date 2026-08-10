from odoo import models
from odoo import fields
from odoo import api
from odoo.exceptions import UserError

class SchoolStudent(models.Model):
    _name = "school.student"
    _description = "School Student Model"

    state = fields.Selection([('draft', 'Draft'), ('active', 'Active'), ('inactive', 'Inactive')], string="State", default='draft')

    first_name = fields.Char(string="First Name", required=True)
    last_name = fields.Char(string="Last Name", required=True)

    full_name = fields.Char(string="String Name")
    student_id = fields.Integer(string="Student ID", required=True)
    gender = fields.Selection([('male', 'Male Student'), ('female', 'Female Student')], string="Gender")
    age = fields.Integer(string="Age")
    phone = fields.Char(string="Phone Number")
    class_id = fields.Many2one('school.class', string="Class")
    teacher_id = fields.Many2one('res.users', string="Teacher")
    is_active_teacher = fields.Boolean(string="Is Active Teacher", related='teacher_id.active', readonly=True)

    def action_activate(self):
        for student in self:
            if student.state == 'draft':
                student.state = 'active'
            else:
                raise UserError("Only students in draft state can be activated.")

    def draft_action(self):
        for student in self:
            if student.state == 'active':
                student.state = 'draft'
            else:
                raise UserError("Only students in active state can be moved to draft.")

    @api.onchange('first_name', 'last_name')
    def onchange_full_name(self):
        if self.first_name and self.last_name:
            self.full_name = self.first_name + ' ' + self.last_name

    @api.constrains('student_id')
    def _check_student_id_and_age(self):
        for student in self:
            if student.student_id and len(str(student.student_id)) > 5:
                raise UserError("Student ID should not exceed 5 digits.")
            if student.student_id and student.age and student.age < 5:
                raise UserError("Student age should be at least 5 years old.")