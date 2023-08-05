# -*- coding: utf-8 -*-
from odoo import fields, models


class FoodCategory(models.Model):
    """
       to manage the categories of food ordered by guest
    """
    _name = "food.category"
    _rec_name = "category"

    category = fields.Char(string="Category",
                           help="Used to create different food items by "
                                "category")
