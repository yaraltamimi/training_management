# -*- coding: utf-8 -*-

from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'
    _description = 'Hotel Guest'

    is_guest = fields.Boolean(string='Is Guest?')