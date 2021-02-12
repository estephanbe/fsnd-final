# Imports
from flask import jsonify, abort, request
from env import SELLER_PER_PAGE
from models import *
from flask_cors import CORS
from helper_functions import *
from env import PRODUCT_PER_PAGE


def get_sellers_route():
    sellers = []
    formated_sellers = []

    try:
        sellers = Seller.query.order_by(Seller.id).all()
        pagenated_sellers = paginated_items(request, sellers, SELLER_PER_PAGE)
    except Exception:
        abort(404)

    if 0 < len(sellers):
        formated_sellers = [p.format() for p in pagenated_sellers]

    

    return jsonify({
        'success': True,
        'sellers': formated_sellers,
        'total_sellers': len(sellers),
    }), 200

def get_seller_route(id):
    body = {}

    try:
        seller = Seller.query.get(id)
    except Exception:
        abort(404, 'seller was not found')

    if seller is None:
        abort(404, 'seller was not found')
    
    related_products = Product.query.filter_by(seller_id=id).all()

    num_of_sales = 0
    for p in related_products:
        num_of_sales += p.num_of_sales
    total_sold_amount = 0
    for p in related_products:
        total_sold_amount += p.total_sales
    
    related_products = [p.format() for p in related_products]
    for p in related_products:
        p['cat'] = Category.query.get(p['cat_id']).format()
        p.pop('cat_id')

    body = {
        'id': seller.id,
        'name': seller.name,
        'phone_number': seller.phone_number,
        'store_description': seller.store_description,
        'avatar': seller.avatar,
        'website': seller.website,
        'facebook_link': seller.facebook_link,
        'registration_date': seller.registration_date,
        'related_products': related_products,
        'total_sold_products': num_of_sales,
        'total_sold_amount': total_sold_amount
    }

    return jsonify(body)

def add_seller_route():
    body = {}
    data = request.get_json()

    # Check if the request was sent empty and abort it.
    if data is None or not len(data):
        abort(422)
    
    if 'avatar' in data and 'facebook_link' in data and 'name' in data and 'phone_number' in data and 'store_description' in data and 'website' in data:
        seller = prepare_seller(data)
    else:
        abort(422, 'One or more of the parameters for adding a seller is missing.')
    
    try:
        seller.insert()
        body["success"] = True
        body["seller_id"] = seller.id
    except Exception:
        abort(422, "The seller was not added.")

    return jsonify(body), 200

def update_seller_route(id):
    data = request.get_json()
    
    try:
        seller = updated_seller(data, id)
        seller.update()
    except Exception:
        abort(422, 'Something went wrong with updating the seller!')

    return jsonify({
        "success": True,
        "seller": seller.format()
    })

def delete_seller_route(id):
    seller = Seller.query.get(id)
    try:
        deleted_seller = seller.delete()
    except Exception:
        abort(422, 'Something went wrong with deleting the seller!')

    return jsonify({
        "success": True,
        "seller": deleted_seller
    })

def seller_search_route():
    q_params = request.args
    
    if "search_term" not in q_params:
        abort(422, "The search term should be included in the query string.")
    
    term = q_params.get("search_term")

    sellers = Seller.query.filter(Seller.name.ilike('%' + term + "%")).all()
    
    return jsonify({
        'sellers_len': len(sellers),
        'sellers': [s.format() for s in sellers]
    })

def get_products_by_seller_route(id):
    products = []
    cats = []
    tags = []
    formated_cats = []
    formated_tags = []

    try:
        products = sorted_products_by_seller(id)
        pagenated_products = paginated_items(request, products, PRODUCT_PER_PAGE)
    except Exception:
        abort(404, 'Couldn\'t find any products related to this category')

    # Cat
    try:
        cats = Category.query.order_by(Category.id).all()
    except Exception:
        abort(404)

    if 0 < len(cats):
        formated_cats = {cat.id: cat.name for cat in cats}
    
    #Tag
    try:
        tags = Tag.query.order_by(Tag.id).all()
    except Exception:
        abort(404)

    if 0 < len(tags):
        formated_tags = {tag.id: tag.name for tag in tags}

    return jsonify({
        'total_products': len(products),
        'success': True,
        'products': [p.format() for p in pagenated_products],
        'cats': formated_cats,
        'tags': formated_tags,
    })

