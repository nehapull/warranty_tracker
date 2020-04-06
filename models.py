import os
from sqlalchemy import Column, String, Date, Integer, Boolean
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
import json

database_name = "warranty"
database_path = "postgres://{}/{}".format('localhost:5432', database_name)

db = SQLAlchemy()
bcrypt = Bcrypt()

'''
setup_db(app): Binds flask app and SQLAlchemy
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    #db.create_all()
     
    migrate = Migrate(app, db)

'''
Product table -- Only keeps track of products that a user wants to keep track of
Rows: id (Integer, primary_key), name (String), date_purchased (Date), warranty_end_date (Date)
If period of warranty is provided then we calculate warranty_end_date and store in DB
'''
class Product(db.Model):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    # TODO: maybe set the default as current date?
    date_purchased = Column(Date)
    warranty_end_date = Column(Date)
    user_id = Column(Integer, db.ForeignKey('users.id', ondelete='CASCADE'))

    # Initialize a product 
    def __init__(self, name, date_purchased, warranty_end_date, user_id):
        self.name = name
        self.date_purchased = date_purchased
        self.warranty_end_date = warranty_end_date
        self.user_id = user_id

    # Insert the product into db
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    # Update the product and commit to db
    def update(self):
        db.session.commit()

    # Delete a product from db and commit changes
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    # Create formatted response for pagination
    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'date_purchased': self.date_purchased,
            'warranty_end_date': self.warranty_end_date,
            'user_id': self.user_id
        }

'''
User table -- Keeps track of whether the user is a buyer or seller (NOTE: not sure if we need this yet 
need to look into Auth0). A Buyer can upload their product to product table, a seller can only upload their item
to the Item table
Rows: id (Integer, primary_key), user_name (String), product_id (db.relationship "Product"), 
isSeller (Boolean)
'''
class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    # Create association with product
    products = db.relationship('Product', backref='user', lazy=True, passive_deletes=True)
    #is_seller = Column(Boolean)
    email = db.Column(String, nullable=False)
    #password = db.Column(String, nullable=False)
    items = db.relationship('Items_for_Sale', backref='user', lazy=True, passive_deletes=True) 

    def __init__(self, name, email):
        self.name = name
        self.email = email
        #self.password = bcrypt.generate_password_hash(password)

    # TODO: add rollback() in try-except block
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def is_correct_password(self, password):
        # This function checks if @arg:password matches the hashed password stored in db
        return bcrypt.check_password_hash(self.password, password)

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'products': User.products
        }

'''
Items_for_Sale table
Rows: id (Integer, primary_key), name (String), warranty_period (Integer), item_description (String), 
image_link (String), phone (String), email (String), user (db.relationship, "User")
'''
class Items_for_Sale(db.Model):
    __tablename__ = 'sell_items'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    warranty_period = Column(Integer)
    item_description = Column(String)
    image_link = Column(String)
    #phone = Column(String)
    #email = Column(String)
    user_id = Column(Integer, db.ForeignKey('users.id', ondelete='CASCADE'))

    def __init__(self, name, warranty_period, item_description, image_link, user_id):
        self.name = name
        self.warranty_period = warranty_period,
        self.item_description = item_description,
        self.image_link = image_link
        self.user_id = user_id
        
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'warranty_period': self.warranty_period,
            'item_description': self.item_description,
            'image_link': self.image_link,
            'user_id': self.user_id
        }

# TODO: April 1st 2020: Create the data models for each table, and start creating endpoints for each table
#       April 2nd 2020: Auth0 + See if you can also incorporate the sellers
#       April 3rd 2020: Start working on frontend -- if taking too much time just use jinja templates
#       April 4th 2020: More frontend + wrap up loose ends
#       April 5th 2020: Buffer day + wrap up loose ends
#       April 6th 2020: Submit capstone


