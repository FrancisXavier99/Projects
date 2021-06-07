import re
from datetime import datetime, date
from odoo import models, fields, api, _, tools
from odoo.exceptions import ValidationError, UserError


class User(models.Model):
    _name = "user.pro"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "About Movies Details"
    _rec_name = "user_name"

    user_no = fields.Char(string="User NO", required=True, track_visibility="always", default=lambda self: _('New'))
    user_name = fields.Char(string="User Name", required=True, track_visibility="always")
    user_age = fields.Integer(string="User Age", required=True, track_visibility="always")
    user_dob = fields.Date(string="User DOB")
    user_gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('others', 'Others')], default='male')
    user_father = fields.Char(string="Father's Name", required=True)
    user_mother = fields.Char(string="Mother's Name", required=True)
    street1 = fields.Char("Street 1", required="1")
    street2 = fields.Char("Street 2")
    city = fields.Char("City")
    state_id = fields.Many2one('res.country.state', string="State")
    country_id = fields.Many2one('res.country', string="Country")
    zip_code = fields.Char("Zip Code")
    mobile_no = fields.Char(string='Mobile No')
    email_id = fields.Char(string='Email Id')

    blood_group = fields.Many2one('blood.details', "Blood Group")

    @api.model
    def create(self, vals):
        if vals.get('user_no', _('New')) == _('New') and self.user_dob == 0:
            vals['user_no'] = self.env['ir.sequence'].next_by_code('olms.user.pro') or _('New')
        result = super(User, self).create(vals)
        return result

    # ********** Name Get Override ********************************

    def name_get(self):
        result = []
        for mo in self:
            if mo.user_name and mo.user_no:
                name = mo.user_name + '( ' + mo.user_no + ' )'
            else:
                name = mo.user_name + '( ' + "Not Defined certificate" + ' )'
            result.append((mo.id, name))
        return result

    # -----------------Age validitation------------
    @api.constrains('user_age')
    def age_constrains(self):
        for rec in self:
            if self.user_age <= 18:
                raise ValidationError(_("Your age must above 18 to book.."))

    # ------------------Email validiaton------------

    @api.onchange('email_id')
    def validate_mail(self):
        if self.email_id and not tools.single_email_re.match(self.email_id):
            raise ValidationError("Email is not valid")

    @api.constrains('mobile_no')
    def validate_mobile(self):
        mo = re.compile("^[6-9]")
        for rec in self:
            if not mo.match(rec.mobile_no) and len(str(rec.mobile_no)) != 10:
                raise ValidationError(_("Invalid Mobile Number"))
            # elif :
            #     raise ValidationError(("Invalid Mobile Number"))
        return True


class EMPLOYEE(models.Model):
    _name = "emp.pro"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "emp_name"

    emp_no = fields.Char(string="Emp NO", required=True, track_visibility="always",
                         default=lambda self: _('New'))
    emp_name = fields.Char("Name")
    emp_gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('others', 'Others')], default="male")
    emp_dob = fields.Date("DOB")
    is_dob = fields.Selection([('age', 'Age'), ('dob', 'DOB')], string="Age or DOB?", default='age', required=True)
    emp_type = fields.Selection([('manager', 'Manager'), ('staff', 'Staff')])
    emp_age = fields.Integer("Age")
    emp_age1 = fields.Char(string="Calculated Age", compute="_calculate_age", store=True)
    emp_email_id = fields.Char("Email_ID")
    emp_mobile_no = fields.Char("Phone Number")
    emp_door_no = fields.Char("Door No")
    emp_father = fields.Char(string="Father's Name", required=True)
    emp_mother = fields.Char(string="Mother's Name", required=True)
    street1 = fields.Char("Street 1", required="1")
    street2 = fields.Char("Street 2")
    city = fields.Char("City")
    state_id = fields.Many2one('res.country.state', string="State")
    country_id = fields.Many2one('res.country', string="Country")
    zip_code = fields.Char("Zip Code")

    blood_group = fields.Many2one('blood.details', "Blood Group")
    lib_id = fields.Many2one('lib.details', "Library")

    # ***************************** Create a orm default sequence*******************
    @api.model
    def create(self, vals):
        if vals.get('emp_no', _('New')) == _('New') and self.emp_dob == 0:
            vals['emp_no'] = self.env['ir.sequence'].next_by_code('olms.emp.pro') or _('New')
        result = super(EMPLOYEE, self).create(vals)
        return result

        # ********** Name Get Override ********************************

    def name_get(self):
        result = []
        for mo in self:
            if mo.emp_name and mo.emp_no:
                name = mo.emp_name + '( ' + mo.emp_no + ' )'
            else:
                name = mo.emp_name + '( ' + "Not Defined certificate" + ' )'
            result.append((mo.id, name))
        return result

    # *******************EMP Date of birth Validate***************************
    @api.onchange('emp_dob')
    def age_onchange(self):
        for rec in self:
            if rec.emp_dob and self.emp_dob > fields.date.today():
                raise ValidationError(_("Please give Valid Date of Birth"))

    # ------------------Date of birth validiation-------------------

    @api.depends('emp_dob')
    def _calculate_age(self):
        print("depends called")
        self.emp_age1 = False
        for rec in self:
            if rec.emp_dob:
                rec.emp_age1 = datetime.now().year - rec.emp_dob.year


class PUBLISHER(models.Model):
    _name = "pub.pro"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "pub_name"

    pub_no = fields.Char(string="Publisher NO", required=True, track_visibility="always",
                         default=lambda self: _('New'))
    pub_name = fields.Char("Name")
    pub_gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('others', 'Others')], default="male")
    pub_dob = fields.Date("DOB")
    is_dob = fields.Selection([('age', 'Age'), ('dob', 'DOB')], string="Age or DOB?", default='age', required=True)
    pub_age = fields.Integer("Age")
    pub_age1 = fields.Char(string="Calculated Age", compute="_calculate_age", store=True)
    pub_email_id = fields.Char("Email_ID")
    pub_mobile_no = fields.Char("Phone Number")
    pub_father = fields.Char(string="Father's Name", required=True)
    pub_mother = fields.Char(string="Mother's Name", required=True)
    street1 = fields.Char("Street 1", required="1")
    street2 = fields.Char("Street 2")
    city = fields.Char("City")
    state_id = fields.Many2one('res.country.state', string="State")
    country_id = fields.Many2one('res.country', string="Country")
    zip_code = fields.Char("Zip Code")

    blood_group = fields.Many2one('blood.details', "Blood Group")
    book_id = fields.Many2one('book.details')

    # ***************************** Create a orm default sequence*******************
    @api.model
    def create(self, vals):
        if vals.get('pub_no', _('New')) == _('New') and self.pub_dob == 0:
            vals['pub_no'] = self.env['ir.sequence'].next_by_code('olms.pub.pro') or _('New')
        result = super(PUBLISHER, self).create(vals)
        return result

        # ********** Name Get Override ********************************

    def name_get(self):
        result = []
        for mo in self:
            if mo.pub_name and mo.pub_no:
                name = mo.pub_name + '( ' + mo.pub_no + ' )'
            else:
                name = mo.pub_name + '( ' + "Not Defined certificate" + ' )'
            result.append((mo.id, name))
        return result

    # *******************Publisher Date of birth Validate***************************
    @api.onchange('pub_dob')
    def age_onchange(self):
        for rec in self:
            if rec.pub_dob and self.pub_dob > fields.date.today():
                raise ValidationError(_("Please Give Valid Date of Birth"))

    # ------------------Date of birth validiation-------------------

    @api.depends('pub_dob')
    def _calculate_age(self):
        print("depends called")
        self.pub_age1 = False
        for rec in self:
            if rec.pub_dob:
                rec.pub_age1 = datetime.now().year - rec.pub_dob.year


class AUTHOR(models.Model):
    _name = "author.pro"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "author_name"

    author_no = fields.Char(string="Author NO", required=True, track_visibility="always",
                            default=lambda self: _('New'))
    author_name = fields.Char("Name")
    author_gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('others', 'Others')], default="male")
    author_dob = fields.Date("DOB")
    is_dob = fields.Selection([('age', 'Age'), ('dob', 'DOB')], string="Age or DOB?", default='age', required=True)
    author_age = fields.Integer("Age")
    author_age1 = fields.Char(string="Calculated Age", compute="_calculate_age", store=True)
    author_email_id = fields.Char("Email_ID")
    author_mobile_no = fields.Char("Phone Number")
    author_father = fields.Char(string="Father's Name", required=True)
    author_mother = fields.Char(string="Mother's Name", required=True)
    street1 = fields.Char("Street 1", required="1")
    street2 = fields.Char("Street 2")
    city = fields.Char("City")
    state_id = fields.Many2one('res.country.state', string="State")
    country_id = fields.Many2one('res.country', string="Country")
    zip_code = fields.Char("Zip Code")

    blood_group = fields.Many2one('blood.details', "Blood Group")
    book_id = fields.Many2one('book.details')

    # ***************************** Create a orm default sequence*******************
    @api.model
    def create(self, vals):
        if vals.get('author_no', _('New')) == _('New') and self.author_dob == 0:
            vals['author_no'] = self.env['ir.sequence'].next_by_code('olms.author.pro') or _('New')
        result = super(AUTHOR, self).create(vals)
        return result

        # ********** Name Get Override ********************************

    def name_get(self):
        result = []
        for mo in self:
            if mo.author_name and mo.author_no:
                name = mo.author_name + '( ' + mo.author_no + ' )'
            else:
                name = mo.author_name + '( ' + "Not Defined certificate" + ' )'
            result.append((mo.id, name))
        return result

    # *******************Author Date of birth Validate***************************
    @api.onchange('author_dob')
    def age_onchange(self):
        for rec in self:
            if rec.author_dob and self.author_dob > fields.date.today():
                raise ValidationError(_("Please give Valid Date of Birth"))

    # ------------------Date of birth validiation-------------------

    @api.depends('author_dob')
    def _calculate_age(self):
        print("depends called")
        self.author_age1 = False
        for rec in self:
            if rec.author_dob:
                rec.author_age1 = datetime.now().year - rec.author_dob.year


class BloodGroup(models.Model):
    _name = 'blood.details'
    _rec_name = 'blood_group'

    blood_group = fields.Char("Blood Group")


class RecordRules(models.Model):
    _inherit = "res.users"

    manager = fields.Many2one("emp.pro", "Manager Role")
    user = fields.Many2one("user.pro", "User Role")
