from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class UpdateBook(models.TransientModel):
    _name = "update.book"

    book_id = fields.Many2one('book.details', string="Choose Book")
    category = fields.Char("Category")
    currency_id = fields.Many2one('res.currency')
    subscrption_amt = fields.Monetary("Subscrption_Amt")


    def Update_Book(self):
        if self.subscrption_amt and self.book_id and self.category:
            self.book_id.write({'category': self.category, 'subscrption_amt': self.subscrption_amt})
        else:
            raise ValidationError(_("Please Enter All The Fields..."))

    # DEFAULT_GET ORM for COUNTRY and STATE and CURRENCY
    @api.model
    def default_get(self, fields):
        data = super(UpdateBook, self).default_get(fields)
        currency_id = self.env['res.currency'].search([('name', '=', 'IN')], limit=1)
        if currency_id:
         data['currency_id'] = currency_id.id
        return data
