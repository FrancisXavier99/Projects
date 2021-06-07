from odoo import models, fields, api, _

class PaymentWizard(models.TransientModel):
    _name = 'payments.wizard'
    _description = "This is the table for Payment wizard"
    _rec_name = 'user_id'

    # name_id = fields.Many2one('buses.details', string="Name", required=True)
    # number = fields.Char(string="Number", required=True)
    # seats = fields.Integer(string="No of Seats", required=True)
    # description = fields.Html(string="Description", required=True)

    user_id = fields.Many2one('booking.details')
    currency_id = fields.Many2one('res.currency')
    total = fields.Monetary(related="user_id.amount_total")
#     payment_seq = fields.Char(related="name_id.payment_seq")
#     date_time = fields.Datetime(related="name_id.date_time")
    
    
    # name_seq_id = fields.Char(related="name_id.name_seq", readonly="True", string="Reference ID")
#     tickets_no = fields.Integer(string="No of Tickets", related="name_id.tickets_no", store=True)
#     total = fields.Monetary(string="Total Amount", related="name_id.total", store=True)


    # DEFAULT_GET ORM for CURRENCY
    @api.model
    def default_get(self, fields):
        data = super(PaymentWizard, self).default_get(fields)
        currency_id = self.env['res.currency'].search([('name', '=', 'INR')], limit=1)
        if currency_id:
            data['currency_id'] = currency_id.id
            return data

    def create_payment(self):
        print("Created")
        return self.env['payments.details'].create({'user_id': self.user_id.id, 'status':'done', 'status_id':'confirm'})
    
    
    
    