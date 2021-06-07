from odoo import models, fields, api, _, tools
from odoo.exceptions import ValidationError, UserError


class Purchase_Order(models.Model):
    _inherit = "purchase.order"

    payed_charges = fields.Monetary("Payed Charges")
    other_charges = fields.Monetary("Other Charges")