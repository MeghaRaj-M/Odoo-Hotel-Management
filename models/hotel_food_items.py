# -*- coding: utf-8 -*-

from odoo import fields, models


class OrderFood(models.Model):
    """ To manage different food items in hotel"""
    _name = "hotel.food.items"
    _rec_name = "food_name"

    food_name = fields.Char(string="Food", help=" Food name")
    category_id = fields.Many2one("food.category",
                                  help="Category which the food belongs")
    food_price = fields.Float(string="Price", help="Price of the food item")
    food_image = fields.Binary(string="Image",
                               help="Image of the food item added")
    food_qty = fields.Integer(string="Quantity",
                              help="Quantity of food item that can be ordered")
    order_id = fields.Many2one("order.food")
    order_record_id = fields.Integer(string="ID")
    currency_id = fields.Many2one('res.currency', readonly=True,
                                  default=lambda self: self.env.company.currency_id)

    def action_order_food(self):
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'hotel.food.items.wizard',
            'target': 'new',
            'context': {'default_food_name': self.food_name,
                        'default_food_price': self.food_price,
                        'default_food_image': self.food_image,
                        'default_category_id': self.category_id.id,
                        'default_order_record_id': self.id
                        }
        }


class OrderFoodWizard(models.TransientModel):
    """ To show food item a wizard when click on kanban"""
    _name = 'hotel.food.items.wizard'

    food_name = fields.Char(string="Food", help=" Food name", readonly=True)
    category_id = fields.Many2one("food.category",
                                  help="Category which the food belongs",
                                  readonly=True)
    food_price = fields.Float(string="Price",
                              help="Price of the food item", readonly=True)
    food_image = fields.Image(string="Image",
                              help="Image of the food item added",
                              readonly=True)
    food_qty = fields.Integer(string="Quantity", default="1",
                              help="Quantity of food item that can be ordered")
    order_record_id = fields.Integer(string="ID")
    currency_id = fields.Many2one('res.currency', readonly=True,
                                  default=lambda self: self.env.company.currency_id)

    def add_food_item(self):
        record_id = self.env.context
        order_record_id = self.env['order.food'].search(
            [('id', '=', record_id['record_id'])])
        order_record_id.update({
            "order_line_ids": [(fields.Command.create({
                    "food_name_id": self.order_record_id,
                    "food_qty": self.food_qty,
                    "sub_total": self.food_price * self.food_qty
            }))]
        })
        order_record_id.room_id.update({
            "list_ids": [(fields.Command.create({
                    "food_name_id": self.order_record_id,
                    "food_qty": self.food_qty,
                    "sub_total": self.food_price * self.food_qty
            }))]
        })
