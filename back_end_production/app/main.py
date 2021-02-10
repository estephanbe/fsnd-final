# Imports
from .routes.product import *
from .routes.seller import *
from .routes.category import *
from .routes.tag import *
from .routes.review import *

from flask import Flask, jsonify
from .helper_functions import *
from .models import *
from .auth import *
from flask_cors import CORS


#=====================================================
# App config

app = Flask(__name__) # setup app
app.config.from_pyfile('config.py') # get configaration
setup_db(app)

cors = CORS(app, resources={r"/*": {"origins": "*"}})

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')

    return response

#=====================================================
# Routes

@app.route('/')
def init():
    return jsonify({
        'success': True,
        'message': 'BoshMall API'
    }), 200

'''
Product Routes
##############
'''

@app.route('/products')
def get_products():
    return get_products_route()

@app.route('/products/<int:id>')
def get_product(id):
    return get_product_route(id)

@app.route('/products', methods=['POST'])
@requires_auth('post:product')
def add_product(payload):
    return add_product_route()

@app.route('/products/<int:id>', methods=["PATCH"])
@requires_auth('update:product')
def update_product(payload, id):
    return update_product_route(id)

@app.route('/products/<int:id>', methods=["DELETE"])
@requires_auth('delete:product')
def delete_product(payload, id):
    return delete_product_route(id)

@app.route('/search', methods=["POST"])
def search():
    return search_route()

@app.route('/sell_products/<int:id>', methods=["PATCH"])
@requires_auth('buy:product')
def sell_product(payload, id):
    return sell_product_route(id)

'''
Seller Routes
##############
'''
@app.route('/sellers')
def get_sellers():
   return get_sellers_route()

@app.route('/sellers/<int:id>')
def get_seller(id):
   return get_seller_route(id)

@app.route('/sellers', methods=['POST'])
@requires_auth('post:product')
def add_seller(payload):
    return add_seller_route()

@app.route('/sellers/<int:id>', methods=["PATCH"])
@requires_auth('update:product')
def update_seller(payload, id):
    return update_seller_route(id)

@app.route('/sellers/<int:id>', methods=["DELETE"])
@requires_auth('delete:product')
def delete_seller(payload, id):
    return delete_seller_route(id)

@app.route('/seller_search', methods=["POST"])
def seller_search():
    return seller_search_route()

@app.route('/sellers/<int:id>/products')
def get_products_by_seller(id):
   return get_products_by_seller_route(id)

'''
Category Routes
##############
'''
@app.route('/categories')
def get_categories():
   return get_categories_route()

@app.route('/categories/<int:id>')
def get_category(id):
   return get_category_route(id)

@app.route('/categories', methods=['POST'])
@requires_auth('post:product')
def add_category(payload):
    return add_category_route()

@app.route('/categories/<int:id>', methods=["PATCH"])
@requires_auth('update:product')
def update_category(payload, id):
    return update_category_route(id)

@app.route('/categories/<int:id>', methods=["DELETE"])
@requires_auth('delete:product')
def delete_category(payload, id):
    return delete_category_route(id)

@app.route('/category_search', methods=["POST"])
def category_search():
    return category_search_route()

@app.route('/categories/<int:id>/products')
def get_products_by_category(id):
   return get_products_by_category_route(id)

'''
Tag Routes
##############
'''
@app.route('/tags')
def get_tags():
   return get_tags_route()

@app.route('/tags/<int:id>')
def get_tag(id):
   return get_tag_route(id)

@app.route('/tags', methods=['POST'])
@requires_auth('post:product')
def add_tag(payload):
    return add_tag_route()

@app.route('/tags/<int:id>', methods=["PATCH"])
@requires_auth('update:product')
def update_tag(payload, id):
    return update_tag_route(id)

@app.route('/tags/<int:id>', methods=["DELETE"])
@requires_auth('delete:product')
def delete_tag(payload, id):
    return delete_tag_route(id)

@app.route('/tag_search', methods=["POST"])
def tag_search():
    return tag_search_route()

@app.route('/tags/<int:id>/products')
def get_products_by_tag(id):
   return get_products_by_tag_route(id)

'''
Review Routes
##############
'''
@app.route('/reviews')
def get_reviews():
   return get_reviews_route()

@app.route('/reviews/<int:id>')
def get_review(id):
   return get_review_route(id)

@app.route('/reviews', methods=['POST'])
@requires_auth('buy:product')
def add_review(payload):
    return add_review_route()

@app.route('/reviews/<int:id>', methods=["PATCH"])
@requires_auth('update:product')
def update_review(payload, id):
    return update_review_route(id)

@app.route('/reviews/<int:id>', methods=["DELETE"])
@requires_auth('delete:product')
def delete_review(payload, id):
    return delete_review_route(id)


'''
Error Handling
##############
'''
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Resource was not found: " + str(error)
    }), 404

@app.errorhandler(401)
def unauthorized_error_handler(error):
    return jsonify({
        "success": False, 
        "error": 401,
        "message": "Unauthorized Access: " + str(error)
    }), 401

@app.errorhandler(422)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable Entity: " + str(error)
    }), 422


@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False, 
        "error": error.error['code'],
        "message": error.error['description']
    }), error.status_code





