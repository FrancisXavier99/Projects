from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class Movie(models.Model):
    _name = "movie.details"
    _description = "About Movies Details"
    _rec_name = "movie_name"

    STATUS_AVAILABLE_LIST = [('available', 'Available'), ('not_available', 'Not Available')]

    movie_firstlook = fields.Image("upload FirstLook")
    movie_name = fields.Char(string="Movie Name")
    language_id = fields.Many2many('res.lang', string="Languages")
    release_date = fields.Date(string="Movie Release Date")
    movie_certificate = fields.Selection([('u', 'U'), ('ua', 'UA'), ('a', 'A')])
    release_country = fields.Selection(
        [('country', 'Country'), ('continent', 'Continent'), ('inter-continent', 'Inter-Continent')])
    actors = fields.Char("Actors")
    music = fields.Char("Music")
    director = fields.Char("Director")
    production = fields.Char("production")
    country_id = fields.Many2one('res.country', string="Country")
    state_id = fields.Many2one('res.country.state', string="State")

    available_status = fields.Selection(STATUS_AVAILABLE_LIST, required=True, default='not_available',
                                        track_visibility='onchange')

    # ****************** url_action **************************************
    def open_trailer_page(self):
        return {
            "type": "ir.actions.act_url",
            "url": "https://www.youtube.com/watch?v=UTiXQcrLlv4",
            "target": "new",
        }

    # ********** Name Get Override ********************************

    def name_get(self):
        result = []
        for mo in self:
            if mo.movie_name and mo.release_country:
                name = mo.movie_name + '( ' + mo.release_country + ' )'
            else:
                name = mo.movie_name + '( ' + "Not Defined certificate" + ' )'
            result.append((mo.id, name))
        return result

    # ************ Release Date Validate ***************************

    @api.onchange('release_date')
    def release_date_onchange(self):
        for rec in self:
            if rec.release_date and self.release_date < fields.date.today():
                raise ValidationError(_("Release Date Must Be futuristic Date..."))

    # *********** Using Default Get Set Value To The Fields***********

    @api.model
    def default_get(self, fields):
        result = super(Movie, self).default_get(fields)
        result['movie_certificate'] = 'ua'
        result['release_country'] = 'inter-continent'
        return result

    # ------------------Server Action------------------------------------------
    def server_action_status_available(self):
        for rec in self:
            if rec.available_status == 'not_available':
                rec.action_available()

    # ----------------------- THIS IS for STATUS BAR-----------------------------------------------------------------
    def action_not_available(self):
        if self.available_status:
            print(self.available_status)
            self.available_status = "not_available"

    def action_available(self):
        if self.available_status:
            print(self.available_status)
            self.available_status = "available"

    # ----------------- This is for Client Action II by Pradison------------------

    @api.model
    def get_movies_info(self):
        # print(self)
        print("get_products_info method called for client action")
        value = []
        dash = {}
        user = []
        data = self.env['movie.details'].search([])
        data1 = self.env['user.details'].search([])
        print(data)
        for rec in data:
            value.append(
                {'name': rec.movie_name, 'language_id': rec.language_id, 'movie_certificate': rec.movie_certificate,
                 'release_date': rec.release_date, 'release_country': rec.release_country,
                 'available_status': rec.available_status})
        for rec in data1:
            user.append(
                {'name': rec.user_name, 'user_age': rec.user_name, 'user_gender': rec.user_gender,
                 'user_dob': rec.user_dob})
        dash.update({'movie':value,'user':user})
        print(value)
        return dash
