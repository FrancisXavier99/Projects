import re
from datetime import datetime, date
from odoo import models, fields, api, _, tools
from odoo.exceptions import ValidationError, UserError


class LIBRARYBOOKISSUE(models.Model):
    _name = "library.book.issue"
    _description = "About Library Book Issue  Details"
    _rec_name = "user_issue_id"

    lib_issue_no = fields.Char(string="LibraryBookIssue NO", required=True, track_visibility="always", default=lambda self: _('New'))
    user_issue_id = fields.Many2one('library.book.card', string="User")
    book_id = fields.Many2one(related='user_issue_id.book_id', string="Book Name")
    total_book = fields.Char(related='user_issue_id.total_book', string="Total Book")
    date_return = fields.Date("Return Date")
    book_issue_date = fields.Date(related="user_issue_id.start_date", string="Book issue Date")
    day_to_return_date = fields.Date(related='user_issue_id.end_date', string="Day TO Return Date")
    actual_return_date = fields.Date("Actual Return Date")
    penalty = fields.Float("Penalty")
    active = fields.Boolean("Active", default=1)

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
