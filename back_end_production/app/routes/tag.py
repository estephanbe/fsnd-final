# Imports
from flask import jsonify, abort, request
from ..models import *
from flask_cors import CORS
from ..helper_functions import *
from ..config import PRODUCT_PER_PAGE


def get_tags_route():
    tags = []

    try:
        tags = Tag.query.order_by(Tag.id).all()
    except Exception:
        abort(404)

    if 0 < len(tags):
        tags = [p.format() for p in tags]

    return jsonify({
        'success': True,
        'tags': tags,
        'total_tags': len(tags),
    }), 200


def get_tag_route(id):
    body = {}

    try:
        tag = Tag.query.get(id)
    except Exception:
        abort(404, 'tag was not found')

    if tag is None:
        abort(404, 'tag was not found')

    products = tag.products

    body = {
        'id': tag.id,
        'name': tag.name,
        'related_products': [p.format() for p in products]
    }

    return jsonify(body)


def add_tag_route():
    body = {}
    data = request.get_json()

    # Check if the request was sent empty and abort it.
    if data is None or not len(data):
        abort(422)

    if 'name' in data:
        if data['name'] == null or data['name'] == '':
            abort(422, 'tag name is missing.')

        tag = Tag(
            name=data['name']
        )
    else:
        abort(
            422,
            'One or more of the parameters for adding a tag is missing.'
        )

    try:
        tag.insert()
        body["success"] = True
        body["tag_id"] = tag.id
    except Exception:
        abort(422, "The tag was not added.")

    return jsonify(body), 200


def update_tag_route(id):
    data = request.get_json()

    try:
        tag = Tag.query.get(id)

        if "name" in data:
            tag.name = data["name"]
            tag.update()
    except Exception:
        abort(422, 'Something went wrong with updating the tag!')

    return jsonify({
        "success": True,
        "tag": tag.format()
    })


def delete_tag_route(id):
    tag = Tag.query.get(id)
    try:
        deleted_tag = tag.delete()
    except Exception:
        abort(422, 'Something went wrong with deleting the tag!')

    return jsonify({
        "success": True,
        "tag": deleted_tag
    })


def tag_search_route():
    q_params = request.args

    if "search_term" not in q_params:
        abort(422, "The search term should be included in the query string.")

    term = q_params.get("search_term")

    tags = Tag.query.filter(Tag.name.ilike('%' + term + "%")).all()

    return jsonify({
        'tags_len': len(tags),
        'tags': [s.format() for s in tags]
    })


def get_products_by_tag_route(id):
    products = []
    cats = []
    tags = []
    formated_cats = []
    formated_tags = []

    '''
    NOTE: I would appreciate if you can teach me how to sort many to many
          relationships
    '''

    try:
        tag = Tag.query.get(id)
        products = tag.products
        pagenated_products = paginated_items(
            request, products, PRODUCT_PER_PAGE)
    except Exception:
        abort(404, 'Couldn\'t find any products related to this tag')

    # Cat
    try:
        cats = Category.query.order_by(Category.id).all()
    except Exception:
        abort(404)

    if 0 < len(cats):
        formated_cats = {cat.id: cat.name for cat in cats}

    # Tag
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
