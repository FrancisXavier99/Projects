import re
from datetime import datetime, date
from odoo import models, fields, api, _, tools
from odoo.exceptions import ValidationError, UserError
from dateutil.relativedelta import relativedelta as rd
from datetime import datetime


class Library(models.Model):
    _name = "library.details"
    _description = "About Lib Details"
    _rec_name = "lib_name"

    lib_no = fields.Char(string="Library NO", track_visibility="always", readonly="1", default=lambda self: _('New'))
    lib_name = fields.Char(string="Library Name", required=True, track_visibility="always")
    lib_email = fields.Char("Library Email")
    lib_mobile = fields.Char("Library Mobile")
    street1 = fields.Char("Street 1", required="1")
    street2 = fields.Char("Street 2")
    city = fields.Char("City")

    book_id = fields.Many2one('book.details', string="Book")
    state_id = fields.Many2one('res.country.state', string="State")
    country_id = fields.Many2one('res.country', string="Country")
    zip_code = fields.Char("Zip Code")

    active = fields.Boolean("Active", default="1")

    # ***************************** Create a orm default sequence*******************
    @api.model
    def create(self, vals):
        if vals.get('lib_no', _('New')) == _('New') and self.lib_mobile == 0:
            vals['lib_no'] = self.env['ir.sequence'].next_by_code('olms.library.details') or _('New')
        result = super(Library, self).create(vals)
        return result

    # ********** Name Get Override ********************************

    def name_get(self):
        result = []
        for mo in self:
            if mo.lib_name and mo.lib_no:
                name = mo.lib_name + '( ' + mo.lib_no + ' )'
            else:
                name = mo.lib_name + '( ' + "Not Defined certificate" + ' )'
            result.append((mo.id, name))
        return result


class LIBRARYBOOKCARD(models.Model):
    _name = "library.book.card"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "About Library Book Card  Details"
    _rec_name = "user_card_id"

    STATUS_LIST = [('confirm', 'Confirm'), ('cancel', 'Cancel')]

    lib_card_no = fields.Char(string="LibraryBookCard No", required=True, track_visibility="always",
                              default=lambda self: _('New'))
    user_card_id = fields.Many2one('user.pro', string="User")
    phone = fields.Char(related="user_card_id.mobile_no", readonly=False, store=True)
    email = fields.Char(related="user_card_id.email_id", readonly=False, store=True)
    status = fields.Selection(STATUS_LIST, required=True, default='cancel')

    book_limit = fields.Integer("Book Limit", default=5)
    date_time = fields.Datetime("Date Time", default=datetime.today())
    duration = fields.Integer("Duration")
    start_date = fields.Date("Starting Date", default=fields.Date.context_today)
    end_date = fields.Date("Ending Date", compute="_compute_end_date", store=True)
    active = fields.Boolean("Active", default="1")
    currency_id = fields.Many2one('res.currency')
    reason = fields.Char("Reason")
    cancel_date = fields.Date("Cancel Date")

    book_line_ids = fields.One2many('library.book.issue', 'book_card_id', track_visibility='always')
    amount_total = fields.Monetary(compute='_amount_all', readonly=True, store=True)

    # ***************************** Create a orm default sequence*******************
    @api.model
    def create(self, vals):
        if vals.get('lib_card_no', _('New')) == _('New'):
            vals['lib_card_no'] = self.env['ir.sequence'].next_by_code('olms.library.book.card') or _('New')
        result = super(LIBRARYBOOKCARD, self).create(vals)
        return result

    # DEFAULT_GET ORM for COUNTRY and STATE and CURRENCY
    @api.model
    def default_get(self, fields):
        data = super(LIBRARYBOOKCARD, self).default_get(fields)
        currency_id = self.env['res.currency'].search([('name', '=', 'IN')], limit=1)
        if currency_id:
            data['currency_id'] = currency_id.id
        return data

    # Ending Date Calcuation
    @api.depends('start_date', 'duration')
    def _compute_end_date(self):
        for rec in self:
            if rec.start_date and rec.duration:
                rec.end_date = rec.start_date + rd(months=rec.duration)

    @api.depends('book_line_ids.sub_total')
    def _amount_all(self):
        print('Total Calculated')
        self.amount_total = False
        for rec in self:

            total = 0
            for line in rec.book_line_ids:
                total += line.sub_total
                rec.update({
                    'amount_total': total,
                })

        # ------------------------ THIS IS for STATUS BAR-------------------------------------------------------------------

    def action_confirm(self):
        template_id = self.env.ref('olms.library_management_system_info_email_corn_templates')
        if self.status:
            template_id.send_mail(self.id, force_send=True)
            self.status = "confirm"
        else:
            print("Mail Could not be sent....!")

    def action_cancel(self):
        if self.status:
            print(self.status)
            self.status = "cancel"

    # ------------------unlink orm----------------------
    def unlink(self):
        if self.available_status == 'cancel':
            print(self.available_status)
            return super(LIBRARYBOOKCARD, self).unlink()
        else:
            ValidationError(_("You Can not delete this record....."))

    # -----------------------This is to send invoice through email---------------------------------------------------

    # def action_send_book_order_invoice_mail(self):
    #
    #     # print("Sending Email to users")
    #     #     template_id = self.env.ref('omtb.movie_ticket_booking_info_email_template').id
    #     #     #                                     addon_name.template id
    #     #     template = self.env['mail.template'].browse(template_id)
    #     #     print(template)
    #     #     #         try:
    #     #     template.send_mail(self.id, force_send=True)
    #     template = self.env.ref('olms.library_management_system_info_email_corn_templates')
    #     print('cron')
    #     if template:
    #         print("Email: inside template")
    #         template.with_context(name="I am context's value").send_mail(self.id, force_send=True)
    #     else:
    #         print("Mail Could not be sent....!")

        # --------------------------Email Corn Sending To Users-----------------------------------

    def mail_sending_template(self):
        print("Cron is called")
        #         register_ids = self.env['orders.details'].search([('date_time', '=', datetime.datetime.today())])
        register_ids = self.env['library.book.card'].search([])
        for rec in register_ids:
            print(rec.email)
            email_to = rec.email
            email_template = self.env.ref('olms.movie_ticket_booking_info_email_corn_template')
            if email_to:
                email_template.send_mail(rec.id, force_send=True)


class LIBRARYBOOKISSUE(models.Model):
    _name = "library.book.issue"
    _description = "About Library Book Issue  Details"
    _rec_name = "book_id"

    lib_issue_no = fields.Char(string="LibraryBookIssue NO", required=True, track_visibility="always",
                               default=lambda self: _('New'))
    book_id = fields.Many2one('book.details', string="Book Name")
    cost = fields.Monetary(related='book_id.subscrption_amt', string="Rent Day Amount")
    total_book = fields.Integer(string="Total Book")
    sub_total = fields.Monetary(compute='_calculate_subtotal', readonly=True, store=True)
    # date_return = fields.Date("Return Date")
    # penalty = fields.Float("Penalty")
    # book_issue_date = fields.Date(related="user_issue_id.start_date", string="Book issue Date")
    # day_to_return_date = fields.Date(related='user_issue_id.end_date', string="Day TO Return Date")
    # actual_return_date = fields.Date("Actual Return Date")
    active = fields.Boolean("Active", default="1")

    currency_id = fields.Many2one('res.currency')
    book_card_id = fields.Many2one('library.book.card')
    # duration = fields.Integer("Duration")

    state = fields.Selection([('draft', 'Draft'), ('issue', 'Issued'),
                              ('reissue', 'Reissued'), ('cancel', 'Cancelled'),
                              ('return', 'Returned'), ('lost', 'Lost'),
                              ('fine', 'Fined'),
                              ('paid', 'Done'),
                              ('subscribe', 'Subscribe'),
                              ('pending', 'Pending'),
                              ],
                             "State", default='draft')

    # ***************************** Create a orm default sequence*******************
    @api.model
    def create(self, vals):
        if vals.get('lib_issue_no', _('New')) == _('New'):
            vals['lib_issue_no'] = self.env['ir.sequence'].next_by_code('olms.library.book.issue') or _('New')
        result = super(LIBRARYBOOKISSUE, self).create(vals)
        return result

    # -------------------DEFAULT_GET ORM for COUNTRY and STATE and CURRENCY---------------
    @api.model
    def default_get(self, fields):
        data = super(LIBRARYBOOKISSUE, self).default_get(fields)
        currency_id = self.env['res.currency'].search([('name', '=', 'IN')], limit=1)
        if currency_id:
            data['currency_id'] = currency_id.id
        return data

    # ----------------_calculate_subtotal----------------------------------
    @api.depends('cost', 'book_card_id.duration', 'total_book')
    def _calculate_subtotal(self):
        print("Sub Totals")
        for rec in self:
            if rec.total_book:
                if rec.cost and rec.book_card_id.duration and rec.total_book:
                    rec.sub_total = rec.total_book * rec.cost * rec.book_card_id.duration
            else:
                print("Duration Totals")
                rec.sub_total = rec.cost * rec.book_card_id.duration

    # -----------------_calculate_book_limit---------------
    @api.onchange('book_card_id.book_limit', 'total_book')
    def _calculate_book_limit(self):
        print("book_limit")
        for rec in self:
            if rec.total_book >= rec.book_card_id.book_limit:
                ValidationError(_("Book Order Limitation 5...."))





class Purchase_Order(models.Model):
    _inherit = "purchase.order"

    @api.onchange('paid_charges', 'other_charges')
    def onchange_paid_amount(self):
        self.tmp_amt = self.paid_charges + self.other_charges

    @api.depends('order_line.price_total', 'tmp_amt')
    def _amount_all(self):
        """
        @override
            overridden to update the paid charges and other amount through temporary amount field."""
        for order in self:
            amount_untaxed = amount_tax = 0.0
            for line in order.order_line:
                line._compute_amount()
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
            order.update({
                'amount_untaxed': order.currency_id.round(amount_untaxed),
                'amount_tax': order.currency_id.round(amount_tax),
                'amount_total': amount_untaxed + amount_tax + order.tmp_amt,
            })


    paid_charges = fields.Monetary("Paid Charges")
    other_charges = fields.Monetary("Other Charges")
    tmp_amt = fields.Float("Temporary Amt", store=True)