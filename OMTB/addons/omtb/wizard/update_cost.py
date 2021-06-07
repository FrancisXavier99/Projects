from odoo import models, fields, api
from odoo.exceptions import UserError


class UpdateMovieCost(models.TransientModel):
    _name = "update.movie.cost"

    movie_id = fields.Many2one('show.details', string="Choose Movie")
    movie_total_amount = fields.Monetary('Amount')
    currency_id = fields.Many2one('res.currency')

    def update_movie_cost(self):
        if self.movie_total_amount:
            self.movie_id.write({'cost': self.movie_total_amount})


 # DEFAULT_GET ORM for COUNTRY and STATE and CURRENCY
    @api.model
    def default_get(self, fields):
        data = super(UpdateMovieCost, self).default_get(fields)
        currency_id = self.env['res.currency'].search([('name', '=', 'IN')], limit=1)
        if currency_id:
            data['currency_id'] = currency_id.id
        return data
