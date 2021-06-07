import re
from odoo import api, models, tools, fields, _
from odoo.exceptions import ValidationError, Warning
from odoo import http
from odoo.http import request


class ControllerClass(http.Controller):

    # ---------------This class is used to fetch book data from DB and display it in tree view--------------------
    @http.route('/books/', auth='public', website=True)
    def index(self, **kw):
        # Model name
        book_data = http.request.env['book.details'].search([])
        # show_data = http.request.env['movie.details'].search([])
        #                                     addon_name.template_id
        print(book_data)
        return http.request.render('olms.book_template', {'book_data': book_data})

    # ---------------------------This is to display the clicked books details widely---------------------------------

    @http.route(['/books/details/<model("book.details"):book_data>'], auth='public', type='http', website=True)
    def books_details(self, book_data):
        values = {'book_data': book_data}
        return request.render("olms.template_books_details", values)

        # --------------------------To Delete record--------------------------------------------------------------------------------------------------------

    @http.route('/books/delete/<int:id>', type="http", auth='user', website=True, method=['GET', 'POST'])
    def books_delete(self, access_token=None, report_type=None, download=False, **post_data):
        if post_data['id']:
            obj = request.env['book.details'].sudo().search([('id', '=', post_data['id'])])
            obj.unlink()
            return http.redirect_with_hash('/')

    # ---------------------------This is for Edit an existing product------------------------------------------------------------------------------------

    @http.route('/books/edit/<int:id>', type='http', auth="public", website=True, csrf=False,
                methods=['GET', 'POST'])
    def edit_book(self, **kw):
        prod = request.env['book.details'].search([('id', '=', kw['id'])])
        # category_id = request.env['category.details'].search([])
        # data = [category_id]
        author_id = request.env['author.pro'].search([])
        publisher_id = request.env['pub.pro'].search([])

        return http.request.render('olms.books_edit',
                                   {'prod': prod, 'author_id': author_id, 'publisher_id': publisher_id})

    # --------------------------To is to save edited products records to book.details object---------------------------------------------------------------------------------------

    @http.route('/books/edit/save', type='http', methods=['POST'], auth="public", website=True, csrf=False)
    def books_edit_save(self, **kw):
        # here in kw you can get the inputted value
        book_name = kw['book_name']
        # image = kw['image']
        subscrption_amt = kw['subscrption_amt']
        category = kw['category']
        author_id = kw['author_id']
        publisher_id = kw['publisher_id']
        publisher_year = kw['publisher_year']
        # author_id = request.env['author.pro'].search([], limit=1)
        # publisher_id = request.env['pub.pro'].search([], limit=1)
        values = {'book_name': book_name, 'category': category, 'author_id': author_id,
                  'publisher_year': publisher_year,
                  'publisher_id': publisher_id,
                  'subscrption_amt': subscrption_amt}
        request.env['book.details'].sudo().search([('id', '=', kw['id'])]).write(values)
        return http.request.render('olms.template_thanks', {})

    # ---------------------------This is for create a new book------------------------------------------------------------------------------------
    @http.route('/books/create', type='http', auth="public", website=True, csrf=False, methods=['GET', 'POST'],
                sitemap=False)
    def create_product(self, **kw):
        book_id = request.env['book.details'].search([])
        author_id = request.env['author.pro'].search([])
        pub_id = request.env['pub.pro'].search([])

        return http.request.render('olms.books_create', {'book_id': book_id, 'author_id': author_id, 'publisher_id': pub_id })

    # --------------------------To is to save products records to book.details object---------------------------------------------------------------------------------------
    @http.route('/books/create/save', type='http', methods=['POST'], auth="public", website=True,
                csrf=False)
    def book_save(self, **kw):
        # here in kw you can get the inputted value
        name = kw['book_name']
        # img = kw['image']
        subscrption_amt = kw['subscrption_amt']
        category = kw['category']
        author_id = kw['author_id']
        publisher_id = kw['publisher_id']
        publisher_year = kw['publisher_year']
        # book_id = request.env['book.details'].search([('id', '=', id)], limit=1)
        values = {'book_name': name, 'category': category,
                  # 'image': img.read().decode('base64'),
                  'subscrption_amt': subscrption_amt,
                  'author_id': author_id,
                  'publisher_id': publisher_id,
                  'publisher_year': publisher_year}
        request.env['book.details'].create(values)
        return http.request.render('olms.template_thanks', {})

    #         return "Thankyou !!"

    # --------------------------This is for create feedback-------------------------------------------------------------------------------------

    @http.route('/feedback', type='http', auth="public", website=True, csrf=False)
    def create_feedback(self, **kw):
        return http.request.render('olms.template_create_feedback')

    # -------------------------Thanks Page-----------------------------------------------------------------------------------------------------------
    #       This is for create a new product
    @http.route('/thanks', type='http', auth="public", website=True, csrf=False)
    def thanks(self, **kw):
        return http.request.render('olms.template_thanks')

    # ------------------------This class is used to fetch user login data from DB and display it in tree view-------------
    @http.route('/user/login', auth='user', type='http', website=True)
    def user_loginview_form(self):
        country = request.env['res.country'].search([])
        state = request.env['res.country.state'].search([])
        blood_group = request.env['blood.details'].search([])
        print(state)
        print(country)
        print(blood_group)
        return request.render("olms.user_login_form",
                              {'state': state, 'country': country, 'blood_group': blood_group})

    @http.route('/user_form', auth='user', type='http', website=True)
    def user_login_form(self, **k):
        print(k)
        name = k['name']
        gender = k['gender']
        age = k['age']
        phone_no = k['phone_no']
        email = k['email']
        father = k['user_father']
        mother = k['user_mother']
        blood = k['blood_group']
        street = k['street1']
        city = k['city']
        zip = k['zip']
        state_id = k['state']
        country_id = k['country']
        request.env['user.pro'].create({
            'user_name': name,
            'user_gender': gender,
            'user_age': age,
            'mobile_no': phone_no,
            'email_id': email,
            'user_father': father,
            'user_mother': mother,
            'blood_group': blood,
            'street1': street,
            'city': city,
            'zip_code': zip,
            'state_id': state_id,
            'country_id': country_id,
        })
        return request.render("olms.booking_success", {})
