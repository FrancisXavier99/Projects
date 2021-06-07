from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, Warning
class DateWizard(models.TransientModel):
    _name = 'date.wizard'
    _description = "This is the table for Date wizard"
#     _rec_name = 'name_id'

    from_date = fields.Datetime(string="From Date", required=True)
    to_date = fields.Datetime(string="To Date", required=True)
    
    # CONSTRAINS DEOCRATOR
    @api.constrains('from_date','to_date')
    def validate_date(self):
        if self.from_date and self.to_date and not self.from_date <= self.to_date:
            raise ValidationError("Choose appropriate dates")


#      To calculate no of days from two given dates
#     @api.onchange('from_date', 'to_date','day_count')
#     def calculate_date(self):
#         if self.from_date and self.to_date:
#             d1=datetime.strptime(str(self.from_date),'%Y-%m-%d') 
#             d2=datetime.strptime(str(self.to_date),'%Y-%m-%d')
#             d3=d2-d1
#             self.day_count= d3.days

        
    def fetch_book_order_details(self):
        self.ensure_one()
        data = {}
        data['ids'] = self.env.context.get('acive_ids', [])
        data['active_model'] = self.env.context.get('active_model', 'ir.ui.menu')
        data['form'] = self.read(['from_date', 'to_date'])[0]
        return self.env.ref('olms.book_order_date_report').report_action(self, data=data)
    
#     Here food.date.report is addo_nname.report_id
    