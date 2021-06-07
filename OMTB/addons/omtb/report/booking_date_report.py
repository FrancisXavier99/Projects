from odoo import fields, models, api
from datetime import datetime
from odoo .exceptions import UserError
# from numpy import record

class DateReport(models.AbstractModel):
    _name = 'report.omtb.movie_booking_date_template'
    # here 'report.passengers.field.report' is folder_name, addon_name and template_name

    def get_data(self, form_values):
        data = []
        from_date = form_values['from_date']
        to_date = form_values['to_date']
        total_all = 0

# here we are using query to get data instead if search ORM
        sql = """ SELECT
                        od.booking_seq, rp.user_name, od.phone, od.email, od.date_time, od.status, od.amount_total
                    FROM
                        booking_details as od
                    LEFT JOIN
                        user_details as rp
                    ON
                        rp.id = od.user_id"""
        self.env.cr.execute(sql, (tuple(self.ids),))
        results = self.env.cr.dictfetchall()
#         print("results")
#         print(results)

        if form_values['from_date'] or form_values['to_date']:
            recordsets = self.env['booking.details'].search([('date_time', '>=', form_values['from_date']), ('date_time', '<=', form_values['to_date'])])

            print("recordsets")
            print(recordsets)
        # for rec in recordsets:
        #     date_time = recordsets.date_time
        for obj in recordsets:
            if obj.status =='confirm' or 'received':
                if obj.amount_total:
                    total_all += obj.amount_total


        for recordsets in recordsets:
            data.append({
                'booking_seq': recordsets.booking_seq,
                'user_id': recordsets.user_id.user_name,
                'phone': recordsets.phone,
                'email': recordsets.email,
                'date_time': recordsets.date_time,
                'amount_total': recordsets.amount_total,
                'total_all': total_all,
#                 'from_date': recordsets.from_date,
# #               'to_date': recordsets.to_date,
            })
#         for rec in results:
#             rec['total_all'] = total_all
#         print(results)
        print(recordsets)
        print(data)
        # import pdb; pdb.set_trace()
        return data

    @api.model
    def _get_report_values(self, docsids, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        return {
            'doc_ids': docsids,
            'doc_model': self.model,
            'data': data['form'],
            'docs': docs,
            'get_data': self.get_data(data['form']),
        }