from odoo import models, fields, api, _, tools
from odoo.exceptions import ValidationError, UserError
from datetime import datetime

class Payments(models.Model):
    _name = "payment.details"
    _inherit = 'mail.thread'
    _description = "About Payments Details"
    _rec_name = "book_order_id"

    STATUS_LIST = [('paid', 'Paid'), ('unpaid', 'Unpaid')]

    book_order_id = fields.Many2one('library.book.card', string="User")
    total = fields.Monetary(related="book_order_id.amount_total")
    payment_seq = fields.Char(string="Payment Reference", required=True, readonly=True, copy=False,
                              index=True, default=lambda self: _('New'))
    payment_status = fields.Selection(STATUS_LIST, required=True, default='unpaid')
    payment_type = fields.Selection([('online', 'Online'), ('code', 'Cash On Hand')])
    date_time = fields.Datetime(default=datetime.today())
    # user_id = fields.Many2one("user.details", string="User")
    currency_id = fields.Many2one('res.currency')
    status_id = fields.Selection(related="book_order_id.status", readonly=False)

    # g_pay = fields.Char(string="Google pay", default="9566970623")
    # phone_pay = fields.Char(string="Theater Phonepe Number", default="8098615996")
    # paytem = fields.Char("Theater Paytem Number", default="8190898998")
    # payment_type = fields.Selection([('google pay', 'Google Pay'), ('phonepe', 'Phone Pe'), ('paytem', 'Paytem')])

    @api.model
    def create(self, vals):
        if vals.get('booking_seq', _('New')) == _('New'):
            vals['payment_seq'] = self.env['ir.sequence'].next_by_code('olms.payment.details') or _('New')
        result = super(Payments, self).create(vals)
        return result

    @api.model
    def default_get(self, fields):
        data = super(Payments, self).default_get(fields)
        currency_id = self.env['res.currency'].search([('name', '=', 'IN')], limit=1)
        if currency_id:
            data['currency_id'] = currency_id.id
        return data

    def action_unpaid(self):
        if self.payment_status:
            print(self.payment_status)
            self.payment_status = "unpaid"

    @api.onchange('payment_status')
    def _onchange_status(self):
        if self.payment_status == 'paid':
            self.status_id = 'confirm'