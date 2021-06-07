from odoo import models, fields, api, _, tools
from odoo.exceptions import ValidationError, UserError
from datetime import datetime


class Booking(models.Model):
    _name = "booking.details"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "user_id"

    STATUS_LIST = [('draft', 'Draft'), ('cancel', 'Cancel'), ('confirm', 'Confirm'), ('received', 'Received')]
    show_type = fields.Selection(
        [('morning show', 'Morning Show'), ('afternoon show', 'Afternoon Show'), ('evening show', 'Evening Show'),
         ('night show', 'Night Show')])

    booking_seq = fields.Char(string="Booking Reference", required=True, readonly=True, copy=False,
                              index=True, default=lambda self: _('New'))
    date_time = fields.Datetime("Date Time", default=datetime.today())
    country_id = fields.Many2one('res.country')
    state_id = fields.Many2one('res.country.state')

    status = fields.Selection(STATUS_LIST, required=True, default='draft')

    currency_id = fields.Many2one('res.currency')
    number_of_ticket = fields.Integer("Number Of Ticket Booking")
    ticket_status = fields.Char("Ticket Status")

    phone = fields.Char(related="user_id.user_mobile_no", readonly=False, store=True)
    email = fields.Char(related="user_id.user_email_id", readonly=False, store=True)
    image = fields.Char()
    cinema_hall_type = fields.Selection(related="cinema_hall_id.cinema_hall_type", readonly=False, store=True,
                                        string="Cinema Screen Type")
    start_time = fields.Datetime(related="show_id.start_time", string="Start Time")
    end_time = fields.Datetime(related="show_id.end_time", string="End Time")

    book_seat_type = fields.Many2one("screenseat.type", string="Book Seat Type")
    movie_id = fields.Many2one("movie.details", string="Movie")
    user_id = fields.Many2one("user.details")
    show_id = fields.Many2one("show.details", string="Movie Shows")

    cinema_hall_id = fields.Many2one("cinemahall.details", string="Cinema Screen")
    payment_id = fields.Many2one("payment.details", string="Payment Type")

    booking_line_ids = fields.One2many('bookingline.details', 'booking_id', track_visibility='always')
    amount_total = fields.Monetary(compute='_amount_all', readonly=True, store=True)

    # ---------------------- CREATE ORM FOR SEQUENCE-----------------------------------------------------------------
    @api.model
    def create(self, vals):
        if vals.get('booking_seq', _('New')) == _('New'):
            vals['booking_seq'] = self.env['ir.sequence'].next_by_code('omtb.booking.details') or _('New')
        result = super(Booking, self).create(vals)
        return result

    # ----------------------- DEFAULT_GET ORM------------------------------------------------------------------
    @api.model
    def default_get(self, fields):
        data = super(Booking, self).default_get(fields)

        country_id = self.env['res.country'].search([('code', '=', 'IN')], limit=1)
        state_id = self.env['res.country.state'].search([('country_id', '=', country_id.id), ('code', '=', 'TN')],
                                                        limit=1)
        currency_id = self.env['res.currency'].search([('name', '=', 'IN')], limit=1)

        if state_id:
            data['state_id'] = state_id.id
        if country_id:
            data['country_id'] = country_id.id or []
        if currency_id:
            data['currency_id'] = currency_id.id
        # data['gender'] = 'male'
        return data

    # --------------------- NAME_GET ORM for Override rec_name--------------------------------------------------------

    def name_get(self):
        result = []
        for rec in self:
            if rec.user_id and rec.booking_seq:
                name_id = rec.user_id.user_name + ' - ' + rec.booking_seq
                result.append((rec.id, name_id))
        return result

    # ------------------------ THIS IS for STATUS BAR-------------------------------------------------------------------

    def action_draft(self):
        if self.status:
            print(self.status)
            self.status = "draft"

    def action_confirm(self):
        if self.status:
            print(self.status)
            self.status = "confirm"

    def action_cancel(self):
        if self.status:
            print(self.status)
            self.status = "cancel"

    def action_received(self):
        if self.status:
            print(self.status)
            self.status = "received"

    # __________________________Movie Fetch to the views__________________________
    def fetch_movies(self):
        print("Fetch movies called")
        return {
            'name': _('Movies'),
            'view_type': 'kanban',
            'res_model': 'movie.details',
            'view_id': False,
            'view_mode': 'kanban',
            'type': 'ir.actions.act_window',
        }

        # -----------------------This is to send invoice through email---------------------------------------------------

    def action_send_booking_invoice_mail(self):

        # print("Sending Email to users")
        #     template_id = self.env.ref('omtb.movie_ticket_booking_info_email_template').id
        #     #                                     addon_name.template id
        #     template = self.env['mail.template'].browse(template_id)
        #     print(template)
        #     #         try:
        #     template.send_mail(self.id, force_send=True)
        template = self.env.ref('omtb.movie_ticket_booking_info_email_template')
        print('cron')
        if template:
            print("Email: inside template")
            template.with_context(name="I am context's value").send_mail(self.id, force_send=True)
        else:
            print("Mail Could not be sent....!")

    # --------------------------Email Corn Sending To Users-----------------------------------

    def mail_sending_template(self):
        print("Cron is called")
        #         register_ids = self.env['orders.details'].search([('date_time', '=', datetime.datetime.today())])
        register_ids = self.env['booking.details'].search([])
        for rec in register_ids:
            print(rec.email)
            email_to = rec.email
            email_template = self.env.ref('omtb.movie_ticket_booking_info_email_corn_template')
            if email_to:
                email_template.send_mail(rec.id, force_send=True)

    @api.depends('booking_line_ids.sub_total')
    def _amount_all(self):
        print('Total Calculated')
        self.amount_total = False
        for rec in self:

            total = 0
            for line in rec.booking_line_ids:
                total += line.sub_total
                rec.update({
                    'amount_total': total,

                })


class BookingLine(models.Model):
    _name = 'bookingline.details'
    _description = 'Booking Line'
    _rec_name = 'show_id'

    # movie_id = fields.Many2one('movie.details', string="Movie", required=True)
    show_id = fields.Many2one('show.details', string="Movie", required=True)
    currency_id = fields.Many2one('res.currency')
    cost = fields.Monetary(related='show_id.cost', string="Cost")
    total_tickets = fields.Integer(string="Total Tickets", default=1)
    sub_total = fields.Monetary(compute='_calculate_subtotal', readonly=True, store=True)
    booking_id = fields.Many2one('booking.details', string="Booking  User")

    @api.depends('cost', 'total_tickets')
    def _calculate_subtotal(self):
        print("Sub Totals")
        for rec in self:
            if rec.cost and rec.total_tickets:
                rec.sub_total = rec.cost * rec.total_tickets

    # DEFAULT_GET ORM for COUNTRY and STATE and CURRENCY
    @api.model
    def default_get(self, fields):
        data = super(BookingLine, self).default_get(fields)
        currency_id = self.env['res.currency'].search([('name', '=', 'IN')], limit=1)
        if currency_id:
            data['currency_id'] = currency_id.id
        return data
