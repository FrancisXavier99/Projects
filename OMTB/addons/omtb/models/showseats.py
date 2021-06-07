from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime

class Show(models.Model):
    _name = "show.details"
    _rec_name = "movie_id"

    show_date = fields.Datetime("Current Date", default=datetime.today())
    show_type = fields.Selection(
        [('morning show', 'Morning Show'), ('afternoon show', 'Afternoon Show'), ('evening show', 'Evening Show'),
         ('night show', 'Night Show')])

    start_time = fields.Datetime("Start Time")
    end_time = fields.Datetime("End Time")
    currency_id = fields.Many2one('res.currency')
    cost = fields.Monetary("Cost")
    seat_status = fields.Char("Seat Status")

    movie_id = fields.Many2one('movie.details', string="Movie Name")
    cinema_hall_id = fields.Many2one('cinemahall.details', string="Cinema Screen")
    # booking_id = fields.Many2one('booking.details', string="Booked")
    # seat_id = fields.Selection(related='cinema_hall_id.seat_type', string="Seat Type")


    @api.onchange('start_time')
    def show_time_onchange(self):
        for rec in self:
            if rec.start_time and self.start_time < fields.datetime.today():
                raise ValidationError(_("Start Date Time Must Be futuristic Date And Time..."))



# DEFAULT_GET ORM for COUNTRY and STATE and CURRENCY
    @api.model
    def default_get(self, fields):
        data = super(Show, self).default_get(fields)
        currency_id = self.env['res.currency'].search([('name', '=', 'IN')], limit=1)
        if currency_id:
            data['currency_id'] = currency_id.id
        return data