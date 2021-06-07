import re, pdb
from datetime import datetime, date
from odoo import models, fields, api, _, tools
from odoo.exceptions import ValidationError, UserError
from dateutil.relativedelta import relativedelta


class User(models.Model):
    _name = "user.details"
    _description = "About Movies Details"
    _rec_name = "user_name"

    user_no = fields.Char(string="User NO", required=True, track_visibility="always", default=lambda self: _('New'))
    user_name = fields.Char(string="User Name", required=True, track_visibility="always")
    user_age = fields.Integer(string="User Age", required=True, track_visibility="always")
    user_dob = fields.Date(string="User DOB")
    user_gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('others', 'Others')], default='male')
    user_mobile_no = fields.Char(string='Mobile No')
    user_email_id = fields.Char(string='Email Id')
    user_country_id = fields.Many2one('res.country', string="Country")
    user_state_id = fields.Many2one('res.country.state', string="State")

    @api.model
    def create(self, vals):
        if vals.get('user_no', _('New')) == _('New') and self.user_dob == 0:
            vals['user_no'] = self.env['ir.sequence'].next_by_code('omtb.user.details') or _('New')
        result = super(User, self).create(vals)
        return result

    # -----------------Age validitation------------
    @api.constrains('user_age')
    def age_constrains(self):
        for rec in self:
            if self.user_age <= 18:
                raise ValidationError(_("Your age must above 18 to book tickets.."))

    # ------------------Email validiaton------------

    @api.onchange('user_email_id')
    def validate_mail(self):
        if self.user_email_id and not tools.single_email_re.match(self.user_email_id):
            raise ValidationError("Email is not valid")

    @api.constrains('user_mobile_no')
    def validate_mobile(self):
        mo = re.compile("^[6-9]")
        for rec in self:
            if not mo.match(rec.user_mobile_no) and len(str(rec.user_mobile_no)) != 10:
                raise ValidationError(_("Invalid Mobile Number"))
            # elif :
            #     raise ValidationError(("Invalid Mobile Number"))
        return True


class Manager(models.Model):
    _name = "manager.details"
    _rec_name = "manager_name"

    manager_no = fields.Char(string="Manager NO", required=True, track_visibility="always",
                             default=lambda self: _('New'))
    manager_name = fields.Char("Name")
    manager_gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('others', 'Others')], default="male")
    manager_dob = fields.Date("DOB")
    is_dob = fields.Selection([('age', 'Age'), ('dob', 'DOB')], string="Age or DOB?", default='age', required=True)

    manager_age = fields.Integer("Age")
    manager_age1 = fields.Char(string="Calculated Age", compute="_calculate_age", store=True)
    manager_email_id = fields.Char("Email_ID")
    manager_phone_no = fields.Char("Phone Number")
    manager_door_no = fields.Char("Door No")
    manager_street_name = fields.Char("Street Name")
    manager_district = fields.Char("District Name")
    manager_country_id = fields.Many2one('res.country', string="Country")
    manager_state_id = fields.Many2one('res.country.state', string="State")

    start_date = fields.Date("Start Date")
    end_date = fields.Date("End Date")
    experience = fields.Char("Experience", compute='calculate_experience', store=True)

    @api.depends('start_date', 'end_date')
    def calculate_experience(self):
        for rec in self:
            if not rec.start_date:
                continue

            date_from = datetime.strptime(str(rec.start_date), "%Y-%m-%d").date()
            date_to = False
            if rec.end_date:
                date_to = datetime.strptime(str(rec.end_date), "%Y-%m-%d").date()
                difference = relativedelta(date_to if date_to else datetime.today().date(), date_from)
                years = difference.years
                months = difference.months
                days = difference.days
                print(years, months, days)
                if (years, months, days != 0):
                    days = '%d days' % (days) if days > 1 else ('%d day' % (days) if days == 1 else '')
                    months = '%d months' % (months) if months > 1 else ('%d month' % (months) if months == 1 else '')
                    years = '%d years' % (years) if years > 1 else ('%d year' % (years) if years == 1 else '')

                rec.experience = (' ' + years if years else '') + (' ' + months if months else '') + days

    # ***************************** Create a orm default sequence*******************
    @api.model
    def create(self, vals):
        if vals.get('manager_no', _('New')) == _('New') and self.manager_dob == 0:
            vals['manager_no'] = self.env['ir.sequence'].next_by_code('omtb.manager.details') or _('New')
        result = super(Manager, self).create(vals)
        return result

    # *******************Manager Date of birth Validate***************************
    @api.onchange('manager_dob')
    def age_onchange(self):
        for rec in self:
            if rec.manager_dob and self.manager_dob > fields.date.today():
                raise ValidationError(_("Please give Valid Date of Birth"))

    # ------------------Date of birth validiation-------------------

    @api.depends('manager_dob')
    def _calculate_age(self):
        print("depends called")
        self.manager_age1 = False
        for rec in self:
            if rec.manager_dob:
                rec.manager_age1 = datetime.now().year - rec.manager_dob.year


class BloodGroup(models.Model):
    _name = 'blood.details'
    _rec_name = 'blood_group'

    blood_group = fields.Char("Blood Group")


class RecordRules(models.Model):
    _inherit = "res.users"

    manager = fields.Many2one("manager.details", "Manager Role")
    user = fields.Many2one("user.details", "User Role")
