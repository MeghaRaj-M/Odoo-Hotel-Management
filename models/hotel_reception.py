# -*- coding: utf-8 -*-
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _, exceptions, Command


class HotelReception(models.Model):
    """ This class is used to create model for managing hotel
    room accommodation and reception"""
    _name = "hotel.reception"
    _description = "Hotel Reception and Accommodation"
    _rec_name = "room_id"
    _inherit = "mail.thread"

    partner_id = fields.Many2one('res.partner', string="Guest",
                                 help="Guest accommodating to hotel")
    number_of_guest = fields.Integer(default=1, string="Number of Guest",
                                     help="Number of guest accommodating "
                                          "in the respective room")
    check_in = fields.Datetime(string="Check In", default=datetime.today(),
                               readonly="True",
                               help="Check in time of guest")
    check_out_date = fields.Datetime(string="Check Out",
                                     compute="_compute_check_out_date",
                                     store=True,
                                     help="check out date and time of guest")
    bed_type = fields.Selection([('single', 'single'), ('double', 'Double'),
                                 ('dormitory', 'Dormitory')], string="Bed Type",
                                help="To select the bed type required by guest")
    facilities_ids = fields.Many2many("room.facility", string="Facility",
                                      help="Facility required by the guest ")
    room_id = fields.Many2one("hotel.management", string="Room",
                              domain="[('state', '!=', 'check_in')]",
                              help="Room available with needed facilities")
    state = fields.Selection([('draft', 'Draft'), ('check_in', 'Check In'),
                              ('check_out', 'Check Out'), ('cancel', 'Cancel')],
                             default='draft', string="State",
                             help="Status of corresponding room")
    reference_no = fields.Char(string=' Sequence', readonly=True,
                               default=lambda self: _('New'))
    expected_days = fields.Integer(string="Expected Days",
                                   help="Number of expected days of stay ")
    expected_date = fields.Date(compute="_computation_expected_date",
                                string="Expected Date", store=True,
                                help="Expected date of check out of  guest")
    name_ids = fields.One2many("guest.information", "guest_id",
                               string="Guest information",
                               help="To get all guest details in the room")
    is_today = fields.Date(default=fields.Date.today(), string="Current date",
                           help="To get the current date")
    is_checked = fields.Boolean(default=True, compute='_compute_is_checked')
    list_ids = fields.One2many("hotel.food.order.list", "add_id")
    invoice_id = fields.Many2one("account.move")
    payment_status = fields.Boolean(default=False, compute='_compute_payment_status')

    @api.model
    def create(self, vals):
        """
           This function is used to create a sequence number which should be
           provided while confirming each accommodation ,
           so we can use it for further reference without any confusion
        """
        if vals.get('reference_no', _('New')) == _('New'):
            vals['reference_no'] = self.env['ir.sequence'].next_by_code(
                'reception_sequence') or _('New')
        res = super(HotelReception, self).create(vals)
        return res

    def mark_as_check_in(self):
        """  To mark accommodation status as check_in
        from draft on clicking button"""
        for record in self:
            if record.number_of_guest == len(self.name_ids):
                record.state = 'check_in'
                record.room_id.state = 'check_in'
            else:
                raise exceptions.UserError(_("Please provide all guest detail"))
            if record.message_main_attachment_id:
                record.state = 'check_in'
                record.room_id.state = 'check_in'
            else:
                raise exceptions.UserError(_("Please add attachment before to "
                                             "check in"))
            return True

    def mark_as_check_out(self):
        """  To mark accommodation status as check_out
         from check in on clicking button"""
        self.state = 'check_out'
        self.room_id.state = 'check_out'
        self.update({
            "list_ids": [(fields.Command.create({
                "description": "Rent",
                "food_qty": (datetime.today() - self.check_in).days if
                (datetime.today() - self.check_in).days > 1 else 1,
                "food_price": self.room_id.rent,
                "sub_total": self.room_id.rent * ((datetime.today() - self.check_in).days
                                                  if (datetime.today() -
                                                      self.check_in).days > 1 else 1)
            }))]
        })
        invoice_lines = []
        for rec in self.list_ids:
            invoice_lines.append((Command.create({
                'name': rec.food_name_id.food_name if rec.food_name_id else "Rent",
                'quantity': rec.food_qty,
                'price_unit': rec.food_price,
                'price_subtotal': rec.sub_total,
            })))
        invoice = self.env['account.move'].create([{
            'move_type': 'out_invoice',
            'partner_id': self.partner_id.id,
            'invoice_line_ids': invoice_lines,
            'invoice_origin': self.reference_no
        }])
        invoice.action_post()
        self.invoice_id = invoice.id
        print(self.invoice_id)
        return {
            'name': 'invoice',
            'view_mode': 'form',
            'res_id': invoice.id,
            'res_model': 'account.move',
            'type': 'ir.actions.act_window',
        }

    @api.depends('invoice_id.payment_state')
    def _compute_payment_status(self):
        for rec in self:
            if rec.invoice_id.payment_state == 'paid':
                rec.payment_status = True
            else:
                rec.payment_status = False

    @api.depends("expected_days")
    def _computation_expected_date(self):
        """ Computed expected date of check out
        with check in and expected days of stay"""
        for record in self:
            record.expected_date = record.check_in + \
                                   relativedelta(days=record.expected_days)

    @api.depends("state")
    def _compute_check_out_date(self):
        """ Calculate check out date on state change"""
        for rec in self:
            rec.check_out_date = datetime.today() if rec.state == 'check_out' else False

    @api.onchange("bed_type", "facilities_ids", "number_of_guest")
    def _bed_type_filter(self):
        """ Filter room based on bed type"""
        domain = [('state', '!=', 'check_in')]
        if self.bed_type == "dormitory":
            domain.append(('available_beds', '>=', self.number_of_guest))
        elif self.bed_type:
            domain.append(('bed', '=', self.bed_type))
            if self.bed_type == "single" and self.number_of_guest != 1:
                self.bed_type = False
                return {'warning': {'message': "Minimum number of "
                                               "accommodation is 1 person"}}
            elif self.bed_type == "double" and self.number_of_guest > 2:
                self.bed_type = False
                return {'warning': {'message': "Minimum number of  "
                                               "accommodation is 2 person"}}
        if self.facilities_ids:
            selected_facilities = self.facilities_ids.ids
            for facility_id in selected_facilities:
                domain.append(('facility_ids', '=', facility_id))
        return {'domain': {'room_id': domain}}

    def _compute_is_checked(self):
        """ To check the expected date of check out and current date matches"""
        for record in self:
            record.is_checked = True if record.is_today == record.expected_date else False

    def action_view_invoice(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoice',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'domain': [('invoice_origin', '=', self.reference_no)],
            'context': "{'create':False}"
        }
