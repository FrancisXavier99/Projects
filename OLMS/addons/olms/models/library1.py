import re
from datetime import datetime, date
from odoo import models, fields, api, _, tools
from odoo.exceptions import ValidationError, UserError

class LIBRARYBOOKCARD(models.Model):
    _name = "library.book.card"
    _description = "About Library Book Card  Details"
    _rec_name = "user_card_id"


    lib_card_no = fields.Char(string="LibraryBookCard No", required=True, track_visibility="always", default=lambda self: _('New'))
    user_card_id = fields.Many2one('user.pro', string="User")
    book_limit = fields.Integer("Book Limit", default= 4)
    total_book =  fields.Char("Total Book")
    book_id =  fields.Many2one('book.details',  string="Book")
    start_date = fields.Date("Starting Date")
    end_date = fields.Date("Ending Date")
    duration = fields.Integer("Duration")
    active = fields.Boolean("Active", default="1")

# ***************************** Create a orm default sequence*******************
    @api.model
    def create(self, vals):
        if vals.get('lib_card_no', _('New')) == _('New'):
            vals['lib_card_no'] = self.env['ir.sequence'].next_by_code('olms.library.book.card') or _('New')
        result = super(LIBRARYBOOKCARD, self).create(vals)
        return result