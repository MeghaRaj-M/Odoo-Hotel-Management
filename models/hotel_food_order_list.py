# -*- coding: utf-8 -*-
from odoo import fields, models


class HotelFoodOrderList(models.Model):
    _name = "hotel.food.order.list"

    food_name_id = fields.Many2one("hotel.food.items", string="Name")
    description = fields.Char(string="Description")
    sub_total = fields.Float(string="sub total")
    food_price = fields.Float(string="Unit Price")
    food_qty = fields.Integer(string="Quantity")
    list_id = fields.Many2one("order.food")
    add_id = fields.Many2one("hotel.reception")
    uom_id = fields.Many2one("uom.uom", string="Uom")
    currency_id = fields.Many2one('res.currency', readonly=True,
                                  default=lambda self: self.env.company.currency_id)
