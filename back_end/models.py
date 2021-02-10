import os
from sqlalchemy import Column, String, Integer, Float, Text, DateTime
from sqlalchemy.sql.schema import ForeignKey
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app):
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db) # config migration

'''
Seller Model
'''
class Seller(db.Model):  
  __tablename__ = 'sellers'

  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(120))
  phone_number = Column(String(120))
  store_description = Column(Text)
  registration_date = Column(DateTime, nullable=False, default=datetime.utcnow)
  avatar = Column(String, nullable=True)
  website = Column(String(120))
  facebook_link = Column(String(120))

  products = db.relationship('Product', backref='seller', lazy=True)


  def __init__(self, name, store_description, phone_number, avatar, website, facebook_link):
    self.name = name
    self.phone_number = phone_number
    self.store_description = store_description
    self.avatar = avatar
    self.website = website
    self.facebook_link = facebook_link
    

  def __repr__(self):
    return f'<{self.id} | {self.name} | {self.store_description} | {self.phone_number} | {self.avatar} | {self.website} | {self.facebook_link}>'

  def insert(self):
    self.registration_date = datetime.now()
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    seller = {
      "id": self.id,
      "name": self.name
    }
    db.session.delete(self)
    db.session.commit()
    return seller

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'phone_number': self.phone_number,
      'store_description': self.store_description,
      'avatar': self.avatar,
      'website': self.website,
      'facebook_link': self.facebook_link
    }

'''
Tag Product Association
'''
tag_product_association = db.Table('tag_product_association',
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True)
)

'''
Product Model
'''
class Product(db.Model):  
  __tablename__ = 'products'

  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(120), nullable=False)
  description = Column(Text, nullable=False)
  creation_date = Column(DateTime, nullable=False, default=datetime.utcnow)
  update_date = Column(DateTime, nullable=False, default=datetime.utcnow)
  price = Column(Float, nullable=False)
  num_of_sales = Column(Integer, default=0)
  total_sales = Column(Float, default=0)
  rating = Column(Integer, default=0)
  image_url = Column(String(120), nullable=True)
  seller_id = Column(Integer, ForeignKey('sellers.id'), nullable=False)
  cat_id = Column(Integer, ForeignKey('categories.id'), nullable=False)

  reviews = db.relationship('Review', backref='product', lazy=True)
  tags = db.relationship('Tag', secondary=tag_product_association, lazy=True,
        backref=db.backref('products', lazy=True))


  def __init__(self, name, description, price, image_url, seller_id, cat_id):
    self.name = name 
    self.description = description
    self.price = price
    self.image_url = image_url 
    self.seller_id = seller_id
    self.cat_id = cat_id

  def __repr__(self):
    return f'<{self.id} | {self.name} | {self.description} | {self.price} | {self.num_of_sales} | {self.total_sales} | {self.rating} | {self.image_url} | {self.seller_id} | {self.cat_id} | {self.creation_date} | {self.update_date}>'

  def insert(self):
    self.creation_date = datetime.utcnow()
    self.update_date = datetime.utcnow()
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    product = {
      "id": self.id,
      "name": self.name
    }
    db.session.delete(self)
    db.session.commit()
    return product

  def format(self):
    return {
        'id': self.id,
        'name': self.name,
        'description': self.description,
        'creation_date': self.creation_date,
        'update_date': self.update_date,
        'price': self.price,
        'num_of_sales': self.num_of_sales,
        'total_sales': self.total_sales,
        'rating': self.rating,
        'image_url': self.image_url,
        'seller_id': self.seller_id,
        'cat_id': self.cat_id,
    }

'''
Tag Model
'''
class Tag(db.Model):
  __tablename__ = 'tags'

  id = Column(Integer, primary_key=True, autoincrement=True)
  name = Column(String(120))

  def __init__(self, name):
        self.name = name

  def __repr__(self):
      return f'<{self.id} | {self.name} >'

  def insert(self):
      db.session.add(self)
      db.session.commit()
  
  def update(self):
      db.session.commit()

  def delete(self):
      tag = {
        "id": self.id,
        "name": self.name
      }
      db.session.delete(self)
      db.session.commit()
      return tag

  def format(self):
      return {
          'id': self.id,
          'name': self.name,
      }

'''
Category Model
'''
class Category(db.Model):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(120))

    products = db.relationship('Product', backref='category', lazy=True)


    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<{self.id} | {self.name} >'

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        cat = {
          "id": self.id,
          "name": self.name
        }
        db.session.delete(self)
        db.session.commit()
        return cat

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
        }


'''
Review Model
'''
class Review(db.Model):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True, autoincrement=True)
    reviewer = Column(String(120), nullable=True)
    review = Column(Text, nullable=False)
    review_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)

    def __init__(self, reviewer, review, product_id):
        self.reviewer = reviewer
        self.review = review
        self.product_id = product_id

    def __repr__(self):
        return f'<{self.id} | {self.reviewer} | {self.review} | {self.review_date} | {self.product_id}>'

    def insert(self):
        self.review_date = datetime.now()
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        cat = {
          "id": self.id,
          "name": self.name
        }
        db.session.delete(self)
        db.session.commit()
        return cat

    def format(self):
        return {
            'id': self.id ,
            'reviewer': self.reviewer ,
            'review': self.review ,
            'review_date': self.review_date ,
            'product_id': self.product_id
        }


