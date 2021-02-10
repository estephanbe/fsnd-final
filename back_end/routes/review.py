# Imports
from flask import jsonify, abort, request
from models import *
from flask_cors import CORS
from helper_functions import *

def get_reviews_route():
    reviews = []

    try:
        reviews = Review.query.order_by(Review.id).all()
    except:
        abort(404)

    if 0 < len(reviews):
        reviews = [p.format() for p in reviews]

    return jsonify({
        'success': True,
        'reviews': reviews,
        'total_reviews': len(reviews),
    }), 200

def get_review_route(id):
    body = {}

    try:
        review = Review.query.get(id)
    except:
        abort(404, 'review was not found')

    if review is None:
        abort(404, 'review was not found')

    body = {
        'id': review.id ,
        'reviewer': review.reviewer ,
        'review': review.review ,
        'review_date': review.review_date ,
        'product_id': review.product_id,
    }

    return jsonify(body)

def add_review_route():
    body = {}
    data = request.get_json()

    # Check if the request was sent empty and abort it.
    if data is None or not len(data):
        abort(422)
    
    if 'reviewer' in data and 'review' in data and 'product_id' in data:
        if data['reviewer'] == null or data['reviewer'] == '':
            abort(422, 'review reviewer is missing.')
        
        if data['review'] == null or data['review'] == '':
            abort(422, 'review review is missing.')
        
        if data['product_id'] == null or data['product_id'] == '':
            abort(422, 'review product_id is missing.')

        review = Review(
            reviewer=data['reviewer'],
            review=data['review'],
            product_id=data['product_id'],
        )
    else:
        abort(422, 'One or more of the parameters for adding a review is missing.')
    
    try:
        review.insert()
        body["success"] = True
        body["review_id"] = review.id
    except:
        abort(422, "The review was not added.")

    return jsonify(body), 200

def update_review_route(id):
    data = request.get_json()

    try:
        review = Review.query.get(id)

        if "review" in data:
            review.review = data["review"]
        
        if "reviewer" in data:
            review.reviewer = data["reviewer"]
        
        if "product_id" in data:
            review.product_id = data["product_id"]
        
        review.update()
    except:
        abort(422, 'Something went wrong with updating the review!')

    return jsonify({
        "success": True,
        "review": review.format()
    })

def delete_review_route(id):
    review = Review.query.get(id)
    try:
        deleted_review = review.delete()
        print(1)
    except:
        abort(422, 'Something went wrong with deleting the review!')

    return jsonify({
        "success": True,
        "review": deleted_review
    })

