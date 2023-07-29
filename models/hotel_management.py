# -*- coding: utf-8 -*-
from odoo import fields, models


class HotelManagement(models.Model):
    """
       In hotel, we have to configure room with room number and other
       facilities available to select while accommodating a person
    """
    _name = "hotel.management"
    _description = "Hotel Managing"
    _rec_name = "room_number"

    room_number = fields.Integer(string="Room Number",
                                 help="Room number for easy accommodation")
    bed = fields.Selection([('single', 'single'), ('double', 'Double'),
                            ('dormitory', 'Dormitory')], string="Bed",
                           help="Type of bed which belongs "
                                "to the respected room")
    available_beds = fields.Float(string="Available Bed",
                                  help="no: of available bed in dormitory ")
    facility_ids = fields.Many2many("room.facility", string="Facilities",
                                    help=" facility in the respected room")
    rent = fields.Monetary(string="Rent(per day)", help="Cost of room for "
                                                        "staying for one day")
    currency_id = fields.Many2one('res.currency', readonly=True,
                                  default=lambda self: self.env.company.currency_id)
    state = fields.Selection([('draft', 'Draft'), ('check_in', 'Check In'),
                              ('check_out', 'Check Out'),
                              ('cancel', 'Cancel')], default='draft',
                             help="Status of corresponding room")
