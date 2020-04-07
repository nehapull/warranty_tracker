"""
This handles the API endpoints and returns responses for appropriate
endpoints.
"""

import os
import requests
from flask import Flask, request, abort, jsonify, redirect, render_template
from flask import session, url_for, make_response
from flask_session.__init__ import Session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from six.moves.urllib.parse import urlencode

from auth import build_login_link, requires_auth, AuthError
from models import setup_db, Product, User, Items_for_Sale

ITEMS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    bcrypt = Bcrypt(app)

    app.secret_key = 'warranty-api'
    token = None

    CORS(app)

    '''
    Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization, true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET, POST, PATCH, DELETE, OPTIONS')

        return response

    '''
    GET request to show homepage and allow user to proceed
    '''
    @app.route('/', methods=['GET'])
    def index():
        return render_template('home.html')

    @app.route('/login')
    def login():
        auth_link = build_login_link()
        return redirect(auth_link, code=302)

    @app.route('/get-token', methods=['POST'])
    def get_token():
        body = request.get_json()
        user_token = body.get('token')

        store_user_session(user_token)

        return jsonify(user_token)

    @app.route('/login-results', methods=['GET'])
    def login_results():
        return render_template('login.html')

    def store_user_session(user_token):
        # Make a request to the userprofile
        token = None
        if user_token.split()[0] == 'Bearer':
            token = user_token
        else:
            token = 'Bearer ' + user_token

        response = requests.get('https://dev-jyqum17r.auth0.com/userinfo',
                                headers={'Authorization': token})
        userinfo = response.json()

        session['token'] = token
        session['jwt_payload'] = userinfo
        session['email'] = userinfo['email']
        session['name'] = userinfo['name']

        # Check if user exists
        user_email = session.get('email')
        user_name = session.get('name')
        user = User.query.filter(User.email == user_email).one_or_none()

        if user is None:
            # User does not exist
            user = User(name=user_name, email=user_email)
            # Insert into database
            user.insert()

    def paginate_products(request, products):
        page = request.args.get('page', 1, type=int)

        if page > len(products):
            abort(404)

        start = (page - 1) * ITEMS_PER_PAGE
        end = start + ITEMS_PER_PAGE

        paginated_products = products[start:end]

        return paginated_products

    def paginate_items(request, items):
        page = request.args.get('page', 1, type=int)

        if page > len(items):
            abort(404)

        start = (page - 1) * ITEMS_PER_PAGE
        end = start + ITEMS_PER_PAGE

        paginated_items = items[start:end]

        return paginated_items

    @app.route('/logout')
    def logout():
        # Clear session stored data
        # session.clear()
        [session.pop(key) for key in list(session.keys())]
        # Redirect user to logout endpoint
        return render_template("home.html")

    # Check if user exists and if not, create the user

    def get_user(request):
        # print(session.get('profile'))
        user_email = session.get('email')
        token = session.get('token')
        if user_email is None or token != request.headers['Authorization']:
            [session.pop(key) for key in list(session.keys())]
            store_user_session(request.headers['Authorization'])
            user_email = session.get('email')

        user = User.query.filter(User.email == user_email).one_or_none()

        if user is None:
            abort(404)

        return user

    @app.route('/products', methods=['GET'])
    @requires_auth('get:products')
    def retrieve_products():
        # Get user info
        user = get_user(request)
        user_id = user.id

        try:
            products = Product.query.filter(Product.user_id == user_id).all()
            formatted_products = [product.format() for product in products]
            paginated_products = paginate_products(request, formatted_products)

            if len(paginated_products) == 0:
                paginated_products = []

            return jsonify({
                'success': True,
                'products': paginated_products,
                'total_products': len(paginated_products)
            })

        except BaseException:
            abort(404)

    @app.route('/products', methods=['POST'])
    @requires_auth('post:products')
    def create_product():
        # Create a new product
        # First retrieve the user in session
        user = get_user(request)
        user_id = user.id

        body = request.get_json()
        if body is None:
            abort(422)

        name = body.get('name', None)
        date_purchased = body.get('date_purchased', None)
        warranty_end_date = body.get('warranty_end_date', None)

        if not name or not date_purchased or not warranty_end_date:
            abort(422)

        try:
            product = Product(
                name=name,
                date_purchased=date_purchased,
                warranty_end_date=warranty_end_date,
                user_id=user_id)

            # Insert product into database
            product.insert()

            products = Product.query.filter(Product.user_id == user_id).all()
            formatted_products = [product.format() for product in products]
            paginated_products = paginate_products(request, formatted_products)

            if len(paginated_products) == 0:
                abort(404)

            return jsonify({
                'success': True,
                'products': paginated_products,
                'total_products': len(paginated_products)
            })

        except BaseException:
            abort(422)

    @app.route('/products/<int:product_id>', methods=['PATCH'])
    @requires_auth('patch:products')
    def update_product(product_id):
        # Retrieve user in session
        user = get_user(request)
        user_id = user.id

        body = request.get_json()

        if body is None:
            abort(422)

        try:
            updated_name = None
            updated_date_purchased = None
            updated_warranty_end = None

            # Find product
            product = Product.query.filter(
                Product.id == product_id).one_or_none()

            if product is None:
                abort(422)

            if 'name' in body:
                updated_name = body.get('name', None)
            else:
                updated_name = product.name

            if 'date_purchased' in body:
                updated_date_purchased = body.get('date_purchased', None)
            else:
                updated_date_purchased = product.date_purchased

            if 'warranty_end_date' in body:
                updated_warranty_end = body.get('warranty_end_date', None)
            else:
                updated_warranty_end = product.warranty_end_date

            product.name = updated_name
            product.date_purchased = updated_date_purchased
            product.warranty_end_date = updated_warranty_end

            product.update()

            products = Product.query.order_by(
                Product.id).filter(
                Product.user_id == user_id).all()
            formatted_products = [product.format() for product in products]
            paginated_products = paginate_products(request, formatted_products)

            return jsonify({
                'success': True,
                'products': paginated_products,
                'total_products': len(paginated_products)
            })

        except BaseException:
            abort(422)

    @app.route('/products/<int:product_id>', methods=['DELETE'])
    @requires_auth('delete:products')
    def delete_product(product_id):
        # Retrieve user
        session.clear()
        user = get_user(request)
        user_id = user.id

        try:
            product = Product.query.filter(
                Product.user_id == user_id).filter(
                Product.id == product_id).one_or_none()

            if product is None:
                abort(404)

            product.delete()

            products = Product.query.filter(Product.user_id == user_id).all()
            formatted_products = [product.format() for product in products]
            paginated_products = paginate_products(request, formatted_products)

            return jsonify({
                'success': True,
                'products': paginated_products,
                'total_products': len(paginated_products)
            })

        except BaseException:
            abort(404)

    # NOTE: we can try to assign seller role based on domain name
    # Requires auth role: 'seller'
    @app.route('/items', methods=['POST'])
    @requires_auth('post:item')
    def create_item():
        # Retrieve user
        user = get_user(request)
        user_id = user.id

        body = request.get_json()
        if body is None:
            abort(422)

        name = body.get('name', None)
        warranty_period = body.get('warranty_period', None)
        item_description = body.get('item_description', None)
        image_link = body.get('image_link', None)

        # Post a new item to sell
        try:
            item = Items_for_Sale(
                name=name,
                warranty_period=warranty_period,
                item_description=item_description,
                image_link=image_link,
                user_id=user_id)

            item.insert()

            items = Items_for_Sale.query.filter(
                Items_for_Sale.user_id == user_id).all()
            formatted_items = [item.format() for item in items]
            paginated_items = paginate_items(request, formatted_items)

            return jsonify({
                'success': True,
                'items': paginated_items,
                'total_items': len(paginated_items)
            })

        except BaseException:
            abort(422)

    @app.route('/items', methods=['GET'])
    @requires_auth('get:items')
    def retrieve_items():
        # Retrieve user
        user = get_user(request)
        user_id = user.id

        # Retrieve items being sold by seller
        try:
            items = Items_for_Sale.query.order_by(
                Items_for_Sale.id).filter(
                Items_for_Sale.user_id == user_id).all()

            formatted_items = [item.format() for item in items]
            paginated_items = paginate_items(request, formatted_items)

            if len(paginated_items) == 0:
                paginated_items = []

            return jsonify({
                'success': True,
                'items': paginated_items,
                'total_items': len(paginated_items)
            })

        except BaseException:
            abort(404)

    @app.route('/items/<int:item_id>', methods=['DELETE'])
    @requires_auth('delete:item')
    def delete_item(item_id):
        # Retrieve user
        user = get_user(request)
        user_id = user.id

        try:
            item = Items_for_Sale.query.filter(
                Items_for_Sale.user_id == user_id).filter(
                Items_for_Sale.id == item_id).one_or_none()

            if item is None:
                abort(404)

            item.delete()

            items = Items_for_Sale.query.order_by(
                Items_for_Sale.id).filter(
                Items_for_Sale.user_id == user_id).all()
            formatted_items = [item.format() for item in items]
            paginated_items = paginate_items(request, formatted_items)

            return jsonify({
                'success': True,
                'items': paginated_items,
                'total_items': len(paginated_items)
            })

        except BaseException:
            abort(404)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'request not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'cannot process request'
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request, try again'
        }), 400

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'internal server error'
        }), 500

    @app.errorhandler(AuthError)
    def authorization_error(error):
        return jsonify({
            'success': False,
            'error': 'AuthError',
            'message': 'Authorization error. Check permissions.'
        }), 403

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
