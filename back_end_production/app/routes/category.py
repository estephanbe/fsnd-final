# Imports
from flask import jsonify, abort, request
from ..models import *
from flask_cors import CORS
from ..helper_functions import *
from ..config import PRODUCT_PER_PAGE

def get_categories_route():
    categories = []

    try:
        categories = Category.query.order_by(Category.id).all()
    except:
        abort(404)

    if 0 < len(categories):
        categories = [p.format() for p in categories]

    return jsonify({
        'success': True,
        'categories': categories,
        'total_categories': len(categories),
    }), 200

def get_category_route(id):
    body = {}

    try:
        category = Category.query.get(id)
    except:
        abort(404, 'category was not found')

    if category is None:
        abort(404, 'category was not found')
    
    products = Product.query.filter_by(cat_id=id).all()

    body = {
        'id': category.id,
        'name': category.name,
        'related_products': [p.format() for p in products]
    }

    return jsonify(body)

def add_category_route():
    body = {}
    data = request.get_json()

    # Check if the request was sent empty and abort it.
    if data is None or not len(data):
        abort(422)
    
    if 'name' in data:
        if data['name'] == null or data['name'] == '':
            abort(422, 'Category name is missing.')

        category = Category(
            name=data['name']
        )
    else:
        abort(422, 'One or more of the parameters for adding a category is missing.')
    
    try:
        category.insert()
        body["success"] = True
        body["category_id"] = category.id
    except:
        abort(422, "The category was not added.")

    return jsonify(body), 200

def update_category_route(id):
    data = request.get_json()

    try:
        category = Category.query.get(id)

        if "name" in data:
            category.name = data["name"]
            category.update()
    except:
        abort(422, 'Something went wrong with updating the category!')

    return jsonify({
        "success": True,
        "category": category.format()
    })

def delete_category_route(id):
    category = Category.query.get(id)
    try:
        deleted_category = category.delete()
    except:
        abort(422, 'Something went wrong with deleting the category!')

    return jsonify({
        "success": True,
        "category": deleted_category
    })

def category_search_route():
    q_params = request.args
    
    if "search_term" not in q_params:
        abort(422, "The search term should be included in the query string.")
    
    term = q_params.get("search_term")

    categories = Category.query.filter(Category.name.ilike('%' + term + "%")).all()
    
    return jsonify({
        'categories_len': len(categories),
        'categories': [s.format() for s in categories]
    })

def get_products_by_category_route(id):
    products = []
    cats = []
    tags = []
    formated_cats = []
    formated_tags = []

    try:
        products = sorted_products_by_cat(id)
        pagenated_products = paginated_items(request, products, PRODUCT_PER_PAGE)
    except:
        abort(404, 'Couldn\'t find any products related to this category')

    # Cat
    try:
        cats = Category.query.order_by(Category.id).all()
    except:
        abort(404)

    if 0 < len(cats):
        formated_cats = {cat.id: cat.name for cat in cats}
    
    #Tag
    try:
        tags = Tag.query.order_by(Tag.id).all()
    except:
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


