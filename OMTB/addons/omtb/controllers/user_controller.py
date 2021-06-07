import re
from odoo import api, models, tools, fields, _
from odoo.exceptions import ValidationError, Warning
from odoo import http
from odoo.http import request


class ControllerClass(http.Controller):

    # This class is used to fetch movie data from DB and display it in tree view
    @http.route('/movies/', auth='public', website=True)
    def index(self, **kw):
        #                                             Model name
        movie_data = http.request.env['movie.details'].search([])
        # show_data = http.request.env['movie.details'].search([])
        #                                     addon_name.template_id
        return http.request.render('omtb.movie_template', {'movie_data': movie_data})

    # ---------------------------This is to display the clicked movies details widely---------------------------------

    @http.route(['/movies/details/<model("movies.details"):movie_data>'], auth='public', type='http', website=True)
    def details_movies(self, movie_data):
        values = {'movie_data': movie_data}
        return request.render("omtb.template_movies_details", values)

    # --------------------------To Delete record--------------------------------------------------------------------------------------------------------
    @http.route('/movies/delete/<int:id>', type="http", auth='user', website=True, method=['GET', 'POST'])
    def movies_delete(self, access_token=None, report_type=None, download=False, **post_data):
        if post_data['id']:
            obj = request.env['movie.details'].sudo().search([('id', '=', post_data['id'])])
            obj.unlink()
            return http.redirect_with_hash('/')

    #             return request.render("food.product_template")

    # ---------------------------This is for Edit an existing product------------------------------------------------------------------------------------

    @http.route('/movies/edit/<int:id>', type='http', auth="public", website=True, csrf=False,
                methods=['GET', 'POST'])
    def edit_movies(self, **kw):
        prod = request.env['movie.details'].search([('id', '=', kw['id'])])
        # category_id = request.env['category.details'].search([])
        # data = [category_id]
        
        return http.request.render('omtb.movies_edit', {'prod': prod})

    # --------------------------To is to save edited products records to products.details object---------------------------------------------------------------------------------------

    @http.route('/movies/edit/save', type='http', methods=['POST'], auth="public", website=True, csrf=False)
    def movies_edit_save(self, **kw):
        # here in kw you can get the inputted value
        movie_name = kw['movie_name']

    #         img = kw['img']
    #         ty = kw['type']
    #         category_id = kw['category_id']
        actors = kw['actors']
    #         description = kw['description']
    #         category_id = request.env['category.details'].search([('id', '=', category_id)], limit=1)
        values = {'movie_name': movie_name, 'actors': actors}
        request.env['movie.details'].sudo().search([('id', '=', kw['id'])]).write(values)
        return http.request.render('omtb.template_thanks', {})

        # --------------------------To is to save products records to products.details object---------------------------------------------------------------------------------------
        @http.route('/movies/create/save', type='http', methods=['POST'], auth="public", website=True, csrf=False)
        def movies_save(self, **kw):
            # here in kw you can get the inputted value
            name = kw['name']
            img = kw['img']
            ty = kw['type']
            category_id = kw['category_id']
            cost = kw['cost']
            description = kw['description']
            category_id = request.env['category.details'].search([('id', '=', category_id)], limit=1)
            values = {'name': name, 'type': ty, 'img': img.read().decode('base64'), 'category_id': kw['category_id'],
                      'cost': cost, 'description': description}
            request.env['movie.details'].sudo().create(values)
            return http.request.render('food.template_thanks', {})
    #         return "Thankyou !!"

    # --------------------------This is for create feedback-------------------------------------------------------------------------------------
    @http.route('/feedback', type='http', auth="public", website=True, csrf=False)
    def create_feedback(self, **kw):
        return http.request.render('omtb.template_create_feedback')

    # -------------------------Thanks Page-----------------------------------------------------------------------------------------------------------
    #       This is for create a new product
    @http.route('/thanks', type='http', auth="public", website=True, csrf=False)
    def thanks(self, **kw):
        return http.request.render('omtb.template_thanks')


# ----------------------------------------------------------------------------------------------------------------------

# @http.route('/list_users', auth='user', type='http', website=True)
# def books_method(self, **kw):
#     student_data = []
#     data = request.env['student.details'].search([])
#     for rec in data:
#         student_data.append({
#             'name_seq': rec.name_seq,
#             'name': rec.name,
#             'dob': rec.dob,
#             'age': rec.age,
#             'gender': rec.gender
#         })
#     print(student_data)
#     return request.render("college.student_details", {'student_data': student_data})

@http.route('/movie_booking', auth='user', type='http', website=True)
def movie_booking_form(self):
    country = request.env['res.country'].search([])
    state = request.env['res.country.state'].search([])
    print(state)
    print(country)
    return request.render("omtb.user_movie_form",
                          {'state': state, 'country': country})


# @api.onchange('age')
# def age_constrains(self):
#     for rec in self:
#         if self.age <= 18:
#             raise ValidationError(_("Your age must above 18 to book tickets.."))
#
# @api.constrains('email')
# def validate_mail(self):
#     if self.email and not tools.single_email_re.match(self.email):
#         raise ValidationError("Email is not valid")
#
# @api.onchange('phone_no')
# def validate_mobile(self):
#     mo = re.compile("^[6-9]")
#     for rec in self:
#         if not mo.match(rec.phone_no) and len(str(rec.phone_no)) != 10:
#             raise ValidationError(_("Invalid Mobile Number"))
#         # elif :
#         #     raise ValidationError(("Invalid Mobile Number"))
#         return True

@http.route('/user_form', auth='user', type='http', website=True)
def user_booking_form(self, **k):
    print(k)
    name = k['name']
    gender = k['gender']
    age = k['age']
    phone_no = k['phone_no']
    email = k['email']
    state_id = k['state']
    country_id = k['country']
    request.env['user.details'].create({
        'user_name': name,
        'user_gender': gender,
        'user_age': age,
        'user_mobile_no': phone_no,
        'user_email_id': email,
        'user_state_id': state_id,
        'user_country_id': country_id,
    })
    return request.render("omtb.booking_success", {})
