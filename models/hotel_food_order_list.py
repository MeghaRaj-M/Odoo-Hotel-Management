# -*- coding: utf-8 -*-
from odoo import fields, models


class HotelFoodOrderList(models.Model):
    _name = "hotel.food.order.list"

    food_name = fields.Many2one("hotel.food.items", string="Name")
    description = fields.Char(string="Description")
    sub_total = fields.Float(string="sub total")
    food_price = fields.Many2one("hotel.food.items", string="Unit Price")
    food_qty = fields.Many2one("hotel.food.items", string="Quantity")
    list_id = fields.Many2one("order.food")



