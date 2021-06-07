import re
from datetime import datetime, date
from odoo import models, fields, api, _, tools
from odoo.exceptions import ValidationError, UserError


class BOOK(models.Model):
    _name = "book.details"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "About book Details"
    _rec_name = "book_name"

    book_no = fields.Char(string="Book NO", required=True, track_visibility="always", default=lambda self: _('New'))
    book_name = fields.Char("Tittle")
    image = fields.Image("Image")
    category = fields.Char("Book Category")
    date_time = fields.Date("Date Time")
    Language_id = fields.Many2many('res.lang', string="Languages")
    author_id = fields.Many2one('author.pro', string="Author")
    publisher_id = fields.Many2one('pub.pro', string="Publisher")
    edition = fields.Char("Edition")
    no_of_page = fields.Char("No Of Pages")
    publisher_year = fields.Date(string="Publisher Year")
    description = fields.Text("Description")
    available_status = fields.Selection([('available', 'Available'),
                                         ('not_available', 'Not Available')],
                                        'Book Availability', default='not_available', track_visibility='onchange')
    availability = fields.Selection([('available', 'Available'),
                                     ('not_available', 'Not Available')],
                                    'Book Availability', default='not_available',
                                    compute="_compute_books_availablity")
    books_available = fields.Float("Books Available",
                                   compute="_compute_books_available")

    is_ebook = fields.Boolean("Is EBook", default="1")
    is_subscription = fields.Boolean("Is Subscription", default="1")
    subscrption_amt = fields.Monetary("Subscription Amount")
    attach_ebook = fields.Binary("Attach EBook")

    currency_id = fields.Many2one('res.currency')
    pub_line_ids = fields.One2many('pub.pro', 'book_id', track_visibility='always')
    author_line_ids = fields.One2many('author.pro', 'book_id', track_visibility='always')

    # ***************************** Create a orm default sequence*******************
    @api.model
    def create(self, vals):
        if vals.get('book_no', _('New')) == _('New') and self.date_time == 0:
            vals['book_no'] = self.env['ir.sequence'].next_by_code('olms.book.details') or _('New')
        result = super(BOOK, self).create(vals)
        return result

    # ********** Name Get Override ********************************
    def name_get(self):
        result = []
        for mo in self:
            if mo.book_name and mo.book_no:
                name = mo.book_name + '( ' + mo.book_no + ' )'
            else:
                name = mo.book_name + '( ' + "Not Defined certificate" + ' )'
            result.append((mo.id, name))
        return result

    # --------------------------defalut orm for the book---------------------------
    @api.model
    def default_get(self, fields):
        data = super(BOOK, self).default_get(fields)
        currency_id = self.env['res.currency'].search([('name', '=', 'IN')], limit=1)
        if currency_id:
            data['currency_id'] = currency_id.id
        # data['gender'] = 'male'
        return data

    # ------------------unlink orm----------------------
    def unlink(self):
        if self.available_status == 'not_available':
            print(self.available_status)
            return super(BOOK, self).unlink()
        else:
            ValidationError(_("You Can not delete this record....."))

    # #-----------------write orm for the book tables-------------------
    #  def write(self, stu):
    #      print(stu)
    #      if self.subscrption_amt == 0:
    #          stu['subscrption_amt'] = 50
    #          result = super(BOOK, self).write(stu)
    #          return result
    #      else:
    #          return super(BOOK, self).write(stu)

    # ------------------Server Action------------------------------------------
    def server_action_status_available(self):
        for rec in self:
            if rec.available_status == 'not_available':
                rec.action_available()

    # ----------------------- THIS IS for STATUS BAR-----------------------------------------------------------------

    def action_not_available(self):
        if self.available_status:
            print(self.available_status)
            self.available_status = "not_available"

    def action_available(self):
        if self.available_status:
            print(self.available_status)
            self.available_status = "available"

    # ---------------------onchange user for validate dates----------------------
    @api.onchange('publisher_year')
    def age_onchange(self):
        for rec in self:
            if rec.publisher_year and self.publisher_year > fields.date.today():
                raise ValidationError(_("Please Enter Correct Publisher Year...."))

        # ----------------- This is for Client Action II by Pradison------------------

    @api.model
    def get_book_info(self):
        # print(self)
        print("get_products_info method called for client action")
        value = []
        dash = {}
        user = []
        data = self.env['book.details'].search([])
        data1 = self.env['user.pro'].search([])
        print(data)
        for rec in data:
            value.append(
                {'book_name': rec.book_name, 'language_id': rec.Language_id, 'category': rec.category,
                 'author_id': rec.author_id.author_name, 'publisher_id': rec.publisher_id.pub_name,
                 'publisher_year': rec.publisher_year,
                 'available_status': rec.available_status})
        for rec in data1:
            user.append(
                {'name': rec.user_name, 'user_age': rec.user_age, 'user_gender': rec.user_gender,
                 'user_dob': rec.user_dob})
        dash.update({'book': value, 'user': user})
        print(value)
        return dash

# @api.depends('qty_available')
# def _compute_books_available(self):
#     '''Computes the available books'''
#     book_issue_obj = self.env['library.book.issue']
#     for rec in self:
#         issue_ids = book_issue_obj.sudo().search([('name', '=', rec.id),
#                                                   ('state', 'in',
#                                                    ('issue', 'reissue'))])
#         occupied_no = 0.0
#         if issue_ids:
#             occupied_no = len(issue_ids)
#         # reduces the quantity when book is issued
#         rec.books_available = rec.qty_available - occupied_no
#     return True
#
#
# @api.depends('books_available')
# def _compute_books_availablity(self):
#     '''Method to compute availability of book'''
#     for rec in self:
#         if rec.books_available >= 1:
#             rec.availability = 'available'
#         else:
#             rec.availability = 'notavailable'
#     return True
