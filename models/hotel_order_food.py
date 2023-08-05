# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import api, fields, models


class OrderFood(models.Model):
    """ To manage the ordering of food by guest"""
    _name = "order.food"
    _rec_name = "room_id"

    room_id = fields.Many2one("hotel.reception", string="Room",
                              domain="[('state', '=', 'check_in')]",
                              help="Room number in which "
                                   "the guest is accommodated")
    partner_id = fields.Many2one(string="Guest", related="room_id.partner_id",
                                 help="Guest in the corresponding room")
    order_time = fields.Datetime(default=datetime.today(), string="Order Time",
                                 help="time in which the guest place the order")
    category_ids = fields.Many2many("food.category", string="Category",
                                    help="food category")
    food_item_ids = fields.One2many("hotel.food.items", "order_id",
                                    compute="_category_wise_food_items",
                                    string="Food", help="Food items available")

    @api.depends('category_ids')
    def _category_wise_food_items(self):
        """ To choose food items based on the category selected"""
        domain = []
        if self.category_ids:
            selected_category = self.env['hotel.food.items'].search(
                [('category_id', 'in', self.category_ids.ids)])
            for food_category in selected_category:
                domain.append(food_category.id)
            self.food_item_ids = domain
        else:
            selected_category = self.env['hotel.food.items'].search(
                [('category_id', '!=', False)])
            for food_category in selected_category:
                domain.append(food_category.id)
            self.food_item_ids = domain

    order_line_ids = fields.One2many("hotel.food.order.list", "list_id")
