from odoo import models, fields


class CinemaTheater(models.Model):
    _name = "theater.details"
    _rec_name = "cinema_theater_name"

    cinema_theater_name = fields.Char("Theater Name")
    cinema_theater_type = fields.Selection([('ac', 'AC'), ('non-ac', 'Non-AC')])
    cinema_theater_parking = fields.Selection([('parking-available', 'Parking-Available'), ('parking-non-available', 'Parking-Non-Available')])
    area_name = fields.Char("Area Name")
    total_cinema_hall = fields.Char("Total No Of Screen")
    city = fields.Char("City")
    district = fields.Char("District Name")
    zip_code = fields.Integer("Pin Code")
    country_id = fields.Many2one('res.country', string="Country")
    state_id = fields.Many2one('res.country.state', string="State")


    # ***************** url_action ***************

    def open_location_page(self):
        return {
            "type": "ir.actions.act_url",
            "url": "https://www.google.com/maps/dir/12.5958014,78.6228498/phoenix+mall+location/@12.820842,77.6052099,9z/data=!3m1!4b1!4m9!4m8!1m1!4e1!1m5!1m1!1s0x3bae11c1a26e7599:0xb8da994f236fbbf0!2m2!1d77.7192343!2d12.9907153",
            "target": "new",
        }



class Cinemahall(models.Model):
    _name = "cinemahall.details"
    _rec_name = "screen_no"

    screen_name = fields.Char("Screen Name")
    cinema_hall_type = fields.Selection([('ac', 'AC'), ('non-ac', 'Non-AC')])
    screen_no = fields.Selection([("1", "1"), ("2", "2"), ("3", "3"), ("4", "4")])
    screen_type = fields.Selection([("2d", "2D"), ("3d", "3D")])
    total_seat = fields.Integer("Total Seat")
    screen_seat_type = fields.Many2many("screenseat.type", string="Screen Seat Type")
    seat_number = fields.Integer("Seat Number")
    cinema_theatre_id = fields.Many2one('theater.details', string="Cinema Theatre")
    manager_id = fields.Many2one('manager.details', string="Manager")


class ScreenSeatType(models.Model):
    _name = "screenseat.type"
    _rec_name = "screen_seat_type"


    screen_seat_type = fields.Char("Screen Seat Type")