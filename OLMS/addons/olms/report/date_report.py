from odoo import fields, models, api
from datetime import datetime
from odoo.exceptions import UserError


# from numpy import record

class DateReport(models.AbstractModel):
    _name = 'report.olms.book_order_date_template'

    # here 'report.passengers.field.report' is folder_name, addon_name and template_name

    def get_data(self, form_values):
        data = []
        from_date = form_values['from_date']
        to_date = form_values['to_date']
        total_all = 0

        # here we are using query to get data instead if search ORM
        # sql = """ SELECT
        #                 od.lib_card_no, rp.user_name, od.phone, od.email, od.start_date, od.status
        #             FROM
        #                 library_book_card as od
        #             LEFT JOIN
        #                 user_pro as rp
        #             ON
        #                 rp.id = od.user_card_id"""
        # self.env.cr.execute(sql, (tuple(self.ids),))
        # results = self.env.cr.dictfetchall()
        #         print("results")
        #         print(results)

        if form_values['from_date'] or form_values['to_date']:
            recordsets = self.env['library.book.card'].search(
                [('date_time', '>=', form_values['from_date']), ('date_time', '<=', form_values['to_date'])])

        for obj in recordsets:
            if obj.status == 'confirm':
                if obj.amount_total:
                    total_all += obj.amount_total
        for rec in recordsets:
            data.append({'lib_card_no': rec.lib_card_no,
                         'user_card_id': rec.user_card_id.user_name,
                         'phone': rec.phone,
                         'email': rec.email,
                         'date_time': rec.date_time,
                         'status': rec.status,
                         'amount_total': rec.amount_total,
                         'total_all': total_all, })
        # for rec in form_values:
        #     rec['total_all'] = total_all
        # print(form_values)
        #         print(data)
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
