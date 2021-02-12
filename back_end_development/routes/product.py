# Imports
from flask import jsonify, abort, request
from models import *
from flask_cors import CORS
from helper_functions import *
from env import PRODUCT_PER_PAGE


def get_products_route():
    products = []
    formated_products = []
    cats = []
    tags = []
    formated_cats = []
    formated_tags = []
    

    # Product
    try:
        products = sorted_products()
        pagenated_products = paginated_items(request, products, PRODUCT_PER_PAGE)
    except Exception:
        abort(404)

    if 0 < len(products):
        formated_products = [p.format() for p in pagenated_products]

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

    
    # Result
    return jsonify({
        'success': True,
        'products': formated_products,
        'total_products': len(products),
        'cats': formated_cats,
        'tags': formated_tags,
    }), 200

def get_product_route(id):
    body = {}

    try:
        product = Product.query.get(id)
    except Exception:
        abort(404, 'Product was not found')

    if product is None:
        abort(404, 'Product was not found')
    
    reviews = Review.query.filter_by(product_id=id).all()
    tags = product.tags
    seller = Seller.query.get(product.seller_id)
    cat = Category.query.get(product.cat_id)

    body = product.format()
    body.pop('seller_id')
    body.pop('cat_id')
    body['seller'] = seller.format()
    body['cat'] = cat.format()
    body['reviews'] = [r.format() for r in reviews]
    body['tags'] = [t.format() for t in tags]

    return jsonify(body)

def add_product_route():
    body = {}
    data = request.get_json()

    # Check if the request was sent empty and abort it.
    if data is None or not len(data):
        abort(422)
    
    if 'name' in data and 'description' in data and 'price' in data and 'image_url' in data and 'seller_id' in data and 'cat_id' in data:
        product = prepare_product(data)
    else:
        abort(422, 'One or more of the parameters for adding a product is missing.')
    
    try:
        product.insert()
        body["success"] = True
        body["product_id"] = product.id
    except Exception:
        abort(422, "The product was not added.")

    return jsonify(body), 200

def update_product_route(id):
    data = request.get_json()

    try:
        product = updated_product(data, id)
        product.update()
    except Exception:
        abort(422, 'Something went wrong with updating the product!')

    return jsonify({
        "success": True,
        "product": product.format()
    })

def delete_product_route(id):
    product = Product.query.get(id)
    try:
        deleted_product = product.delete()
    except Exception:
        abort(422, 'Something went wrong with deleting the product!')

    return jsonify({
        "success": True,
        "product": deleted_product
    })

def search_route():
    # search will be for products:
    # the search will be looking into the following:
        # The name of the product
        # The description of the product
        # The name of a category
            # extract the category id based on the reulted name
            # get all the products with the category id
        # The name of a tag
            # get all the products related to each tag
        # The review
            # get all the products related to each review
    # sort the resulted products by default num_of_sales, and provide the option to sort by the columns
    final_products = []
    q_params = request.args
    
    if "search_term" not in q_params:
        abort(422, "The search term should be included in the query string.")
    
    term = q_params.get("search_term")

    p_from_products = Product.query.filter(Product.name.ilike('%' + term + "%")).all()
    p_from_products_description = Product.query.filter(Product.description.ilike('%' + term + "%")).all()
    p_from_products = {p.id: p for p in p_from_products}
    p_from_products_description = {p.id: p for p in p_from_products_description}
    
    cats = Category.query.filter(Category.name.ilike('%' + term + "%")).all()
    p_from_cats = {}
    for cat in cats:
        related_products = Product.query.filter_by(cat_id=cat.id).all()
        if 0 < len(related_products):
            for p in related_products:
                p_from_cats[p.id] = p
    
    reviews = Review.query.filter(Review.review.ilike('%' + term + "%")).all()
    p_from_reviews = {}
    for review in reviews:
        related_products = Product.query.filter_by(id=review.product_id).all()
        if 0 < len(related_products):
            for p in related_products:
                p_from_reviews[p.id] = p
    
    tags = Tag.query.filter(Tag.name.ilike('%' + term + "%")).all()
    p_from_tags = {}
    for tag in tags:
        related_products = tag.products
        if 0 < len(related_products):
            for p in related_products:
                p_from_tags[p.id] = p

    final_products = dict(p_from_products)
    final_products.update(p_from_products_description)
    final_products.update(p_from_cats)
    final_products.update(p_from_reviews)
    final_products.update(p_from_tags)

    final_products = [value.format() for key, value in final_products.items()]

    return jsonify({
        'products_len': len(final_products),
        'products': final_products
    })

def sell_product_route(id):
    try:
        product = Product.query.get(id)
    except Exception:
        abort(404, "Product was not found")
    
    
    product.num_of_sales += 1
    product.total_sales += product.price

    try:
        product.update()
    except Exception:
        abort(422, "Product sale was not updated")

    return jsonify(product.format())
    