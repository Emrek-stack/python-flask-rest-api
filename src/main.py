import os
import datetime
from flask import Blueprint, Flask, request
from flask_restplus import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from api.account import HelloWorld


api = Api()
app = Flask(__name__)

DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user="postgres",pw="mysecretpassword",url="192.168.99.100:5432",db="firefly")

#SQL Alchemyaoo
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db = SQLAlchemy(app)

# entities
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    username = db.Column(db.String(32), index = True)
    password_hash = db.Column(db.String(128))
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)    
    name = db.Column(db.String(32), index = True)
    addresses = db.relationship('customer_address', backref='customer', lazy=True)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

class CustomerAddress(db.Model):
    __tablename__ = 'customer_address'
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    address = db.Column(db.String(128))    

api.init_app(app)



# def create_user
##@app.cli.command('resetdb')
def resetdb_command():
    """Destroys and creates the database + tables."""

    from sqlalchemy_utils import database_exists, create_database, drop_database
    if database_exists(DB_URL):
        print('Deleting database.')
        drop_database(DB_URL)
    if not database_exists(DB_URL):
        print('Creating database.')
        create_database(DB_URL)

    #db.drop_all()
    print('Creating tables.')
    db.create_all()
    print('Shiny!')


#api
#user methods
@api.route('/login', methods=["POST"])
def login():
    print(request)
    return "aa"
    


if __name__ == '__main__':
    resetdb_command()
    app.run(debug=True)


