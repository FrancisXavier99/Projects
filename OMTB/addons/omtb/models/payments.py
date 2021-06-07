from odoo import models, fields, api, _, tools
from odoo.exceptions import ValidationError, UserError
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta



class Payments(models.Model):
    _name = "payments.details"
    _inherit = 'mail.thread'
    _description = "About Payments Details"
    _rec_name = "booking_id"

    STATUS_LIST = [('draft', 'Draft'), ('done', 'Done')]

    booking_id = fields.Many2one('booking.details', string="User")
    total = fields.Monetary(related="booking_id.amount_total")
    payment_seq = fields.Char(string="Payment Reference", required=True, readonly=True, copy=False,
                              index=True, default=lambda self: _('New'))
    status = fields.Selection(STATUS_LIST, required=True, default='draft')
    date_time = fields.Datetime(default=datetime.today())
    user_id = fields.Many2one("user.details", string="User")
    currency_id = fields.Many2one('res.currency')
    status_id = fields.Selection(related="booking_id.status", readonly=False)
    start_date = fields.Date("Start Date")
    end_date = fields.Date("End Date")
    exper = fields.Char("Experience",compute='calculate_experience', store=True)

    # g_pay = fields.Char(string="Google pay", default="9566970623")
    # phone_pay = fields.Char(string="Theater Phonepe Number", default="8098615996")
    # paytem = fields.Char("Theater Paytem Number", default="8190898998")
    # payment_type = fields.Selection([('google pay', 'Google Pay'), ('phonepe', 'Phone Pe'), ('paytem', 'Paytem')])

    @api.model
    def create(self, vals):
        if vals.get('booking_seq', _('New')) == _('New'):
            vals['payment_seq'] = self.env['ir.sequence'].next_by_code('omtb.payments.details') or _('New')
        result = super(Payments, self).create(vals)
        return result

    @api.model
    def default_get(self, fields):
        data = super(Payments, self).default_get(fields)
        currency_id = self.env['res.currency'].search([('name', '=', 'IN')], limit=1)
        if currency_id:
            data['currency_id'] = currency_id.id
        return data

    def action_draft(self):
        if self.status:
            print(self.status)
            self.status = "draft"

    @api.onchange('status')
    def _onchange_status(self):
        if self.status == 'done':
            self.status_id = 'confirm'

    @api.depends('start_date', 'end_date')
    def calculate_experience(self):
        print("holoo")
        for rec in self:
            if rec.start_date and rec.end_date:
                rec.exper= rec.start_date - relativedelta(months=int(rec.end_date))
                print(rec.exper)

        # fmt = '%Y-%m-%d'
        # start_date = self.start_date
        # end_date = self.end_date
        # d1 = datetime.strptime(start_date, fmt).date()
        # d2 = datetime.strptime(end_date, fmt).date()
        # self.experience = relativedelta(d2, d1)
        # print(self.experience.years)
        # print(self.experience.months)
        # print(self.experience.days)
        # if d2 > d1:
        #     self.experience = (d2 - d1).days
        # else:
        #     raise ValueError('end date should be superior than start day')
