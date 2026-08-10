# -*- coding: utf-8 -*-

from odoo import models, fields


class HotelRoom(models.Model):
    _name = 'hotel.room'
    _description = 'Hotel Room'

    name = fields.Char(string="Room Name", required=True)
    capacity = fields.Integer(string="Capacity")
    is_reserved = fields.Boolean(string="Is Reserved?")


class HotelReservation(models.Model):
    _name = 'hotel.reservation'
    _description = 'Hotel Reservation'

    name = fields.Char(string="Reservation Name", required=True)
    date_from = fields.Datetime(string="Date From")
    date_to = fields.Datetime(string="Date To")
    duration = fields.Integer(string="Duration")

    # Relationships (Many2one) with Domain for Guests
    guest_id = fields.Many2one(
        'res.partner', 
        string="Guest", 
        domain="[('is_guest', '=', True)]", 
        required=True
    )
    room_id = fields.Many2one(
        'hotel.room', 
        string="Room", 
        required=True
    )