# -*- coding: utf-8 -*-
from odoo import models, fields, api

class GymMember(models.Model):
    _name = 'gym.member'
    _description = 'Gym Member'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    member_name = fields.Char(string="Name", required=True)
    age = fields.Integer(string="Age")
    join_date = fields.Date(string="Join Date")
    is_active = fields.Boolean(string="Is Active", default=True)
    
    membership_type = fields.Selection(
        [
            ('monthly', 'Monthly'),
            ('yearly', 'Yearly'),
        ], string="Membership Type",
    )
    
    training_type = fields.Selection(
        [
            ('personal', 'Personal Training'),
            ('group', 'Group Training'),
        ], string="Training Type", default='personal',
    )
    
    subscription_fee = fields.Float(string="Subscription Fee")
    health_notes = fields.Text(string="Health Notes")
    member_photo = fields.Binary(string="Photo")
    test_field = fields.Char(string="Test Field")

    @api.onchange('membership_type', 'training_type')
    def _onchange_membership_type(self):
        
        if self.membership_type == 'monthly':
            if self.training_type == 'personal':
                self.subscription_fee = 1400.0
            else:  # group
                self.subscription_fee = 300.0
        
        elif self.membership_type == 'yearly':
            if self.training_type == 'personal':
                self.subscription_fee = 7000.0
            else:  # group
                self.subscription_fee = 2400.0
        
        else:
            self.subscription_fee = 0.0