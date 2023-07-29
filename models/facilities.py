# -*- coding: utf-8 -*-
from odoo import fields, models


class FacilityModel(models.Model):
    """
       In managing hotel , have to provide different facilities for room
       so that the customer can choose the room according to the
       facilities they need
    """
    _name = "room.facility"
    _rec_name = "facility"
    _description = "Room Facilities"

    facility = fields.Char(string="Facility", help="To add different facility "
                                                   "needed while choosing the"
                                                   " room")

