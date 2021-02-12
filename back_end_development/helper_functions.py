from flask import abort, request
import json
from sqlalchemy.sql.expression import null
from models import Product, Seller, Tag
from datetime import datetime
import sys 
import http.client
from env import *


def paginated_items(request, products, per_page):
  page = int(request.args.get('page', 1))
  start = (page - 1) * per_page
  end = start + per_page

  return products[start:end]

def prepare_product(data):
    if data['name'] == null or data['name'] == '':
        abort(422, 'Product name is missing.')
    
    if data['description'] == null or data['description'] == '':
        abort(422, 'Product description is missing.')
    
    if data['price'] == null or data['price'] == 0:
        abort(422, 'Product price is missing or equal 0.')
    
    if data['seller_id'] == null or data['seller_id'] == 0:
        abort(422, 'Product\'s seller ID is missing.')
    
    if data['cat_id'] == null or data['cat_id'] == 0:
        abort(422, 'Product\'s category ID is missing.')

    product = Product(
        name=data['name'],
        description=data['description'],
        price=data['price'],
        image_url=data['image_url'],
        seller_id=data['seller_id'],
        cat_id=data['cat_id']
    )

    return product

def updated_product(data, id):
    product = Product.query.get(id)

    if "name" in data:
        product.name = data["name"]
    
    if "description" in data:
        product.description = data["description"]
    
    if "price" in data:
        product.price = data["price"]

    if "rating" in data:
        product.rating = data["rating"]

    if "image_url" in data:
        product.image_url = data["image_url"]

    if "seller_id" in data:
        product.seller_id = data["seller_id"]

    if "cat_id" in data:
        product.cat_id = data["cat_id"]

    if data is not None and data is not null and bool(data):
        product.update_date = datetime.utcnow()

    return product

def prepare_seller(data):
    if data['name'] == null or data['name'] == '':
        abort(422, 'Seller name is missing.')
    
    if data['phone_number'] == null or data['phone_number'] == '':
        abort(422, 'Seller phone_number is missing.')
    
    if data['store_description'] == null or data['store_description'] == 0:
        abort(422, 'Seller store_description is missing or equal 0.')
    
    if data['avatar'] == null or data['avatar'] == 0:
        abort(422, 'Seller\'s avatar is missing.')
    
    if data['website'] == null or data['website'] == 0:
        abort(422, 'Seller\'s website is missing.')

    if data['facebook_link'] == null or data['facebook_link'] == 0:
        abort(422, 'Seller\'s facebook link is missing.')

    seller = Seller(
        name=data['name'],
        phone_number=data['phone_number'],
        store_description=data['store_description'],
        avatar=data['avatar'],
        website=data['website'],
        facebook_link=data['facebook_link']
    )

    return seller

def updated_seller(data, id):
    seller = Seller.query.get(id)

    if "name" in data:
        seller.name = data["name"]
    
    if "phone_number" in data:
        seller.phone_number = data["phone_number"]
    
    if "store_description" in data:
        seller.store_description = data["store_description"]

    if "avatar" in data:
        seller.avatar = data["avatar"]

    if "website" in data:
        seller.website = data["website"]

    if "facebook_link" in data:
        seller.facebook_link = data["facebook_link"]

    return seller

def sorted_products():
    q_params = request.args
    sorting = q_params.get("sort", None)

    products = []

    try:
        if (sorting != None and sorting == 'dateN'):
            products = Product.query.order_by(Product.creation_date.desc()).all()
        elif (sorting != None and sorting == 'dateO'):
            products = Product.query.order_by(Product.creation_date).all()
        elif (sorting != None and sorting == 'priceL'):
            products = Product.query.order_by(Product.price).all()
        elif (sorting != None and sorting == 'priceH'):
            products = Product.query.order_by(Product.price.desc()).all()
        elif (sorting != None and sorting == 'ratingL'):
            products = Product.query.order_by(Product.rating).all()
        elif (sorting != None and sorting == 'ratingH'):
            products = Product.query.order_by(Product.rating.desc()).all()
        elif (sorting != None and sorting == 'salesL'):
            products = Product.query.order_by(Product.num_of_sales).all()
        elif (sorting != None and sorting == 'salesH'):
            products = Product.query.order_by(Product.num_of_sales.desc()).all()
        else:
            products = Product.query.order_by(Product.id).all()
    except Exception:
        print(sys.exc_info())
    
    return products

def sorted_products_by_cat(id):
    q_params = request.args
    sorting = q_params.get("sort", None)

    products = []

    try:
        if (sorting != None and sorting == 'dateN'):
            products = Product.query.filter_by(cat_id=id).order_by(Product.creation_date.desc()).all()
        elif (sorting != None and sorting == 'dateO'):
            products = Product.query.filter_by(cat_id=id).order_by(Product.creation_date).all()
        elif (sorting != None and sorting == 'priceL'):
            products = Product.query.filter_by(cat_id=id).order_by(Product.price).all()
        elif (sorting != None and sorting == 'priceH'):
            products = Product.query.filter_by(cat_id=id).order_by(Product.price.desc()).all()
        elif (sorting != None and sorting == 'ratingL'):
            products = Product.query.filter_by(cat_id=id).order_by(Product.rating).all()
        elif (sorting != None and sorting == 'ratingH'):
            products = Product.query.filter_by(cat_id=id).order_by(Product.rating.desc()).all()
        elif (sorting != None and sorting == 'salesL'):
            products = Product.query.filter_by(cat_id=id).order_by(Product.num_of_sales).all()
        elif (sorting != None and sorting == 'salesH'):
            products = Product.query.filter_by(cat_id=id).order_by(Product.num_of_sales.desc()).all()
        else:
            products = Product.query.filter_by(cat_id=id).all()
    except Exception:
        print(sys.exc_info())
    
    return products

def sorted_products_by_seller(id):
    q_params = request.args
    sorting = q_params.get("sort", None)

    products = []

    try:
        if (sorting != None and sorting == 'dateN'):
            products = Product.query.filter_by(seller=id).order_by(Product.creation_date.desc()).all()
        elif (sorting != None and sorting == 'dateO'):
            products = Product.query.filter_by(seller=id).order_by(Product.creation_date).all()
        elif (sorting != None and sorting == 'priceL'):
            products = Product.query.filter_by(seller=id).order_by(Product.price).all()
        elif (sorting != None and sorting == 'priceH'):
            products = Product.query.filter_by(seller=id).order_by(Product.price.desc()).all()
        elif (sorting != None and sorting == 'ratingL'):
            products = Product.query.filter_by(seller=id).order_by(Product.rating).all()
        elif (sorting != None and sorting == 'ratingH'):
            products = Product.query.filter_by(seller=id).order_by(Product.rating.desc()).all()
        elif (sorting != None and sorting == 'salesL'):
            products = Product.query.filter_by(seller=id).order_by(Product.num_of_sales).all()
        elif (sorting != None and sorting == 'salesH'):
            products = Product.query.filter_by(seller=id).order_by(Product.num_of_sales.desc()).all()
        else:
            products = Product.query.filter_by(seller=id).all()
    except Exception:
        print(sys.exc_info())
    
    return products
