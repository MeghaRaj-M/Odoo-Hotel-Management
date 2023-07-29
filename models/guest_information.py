# -*- coding: utf-8 -*-

from odoo import fields, models


class GuestInformation(models.Model):
    """
     This class is used to create a model for collecting the information of
     all the guests who check-in
    """
    _name = "guest.information"

    name = fields.Char(string="Name", help="Name of the guest check in")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')],
                              string="Gender",
                              help="Gender of each guest check in")
    age = fields.Integer(string="Age", help="Age of guest check in")
    guest_id = fields.Many2one("hotel.reception", required="True")
