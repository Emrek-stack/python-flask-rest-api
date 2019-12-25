import os
import datetime
import json
from flask import Flask, request, make_response, jsonify
from flask_restplus import Resource, Api, fields, marshal_with, marshal
from flask_sqlalchemy import SQLAlchemy
from passlib.apps import custom_app_context as pwd_context
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt, JWTManager)

app = Flask(__name__)
api = Api(app)

#jwt settings
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
jwt = JWTManager(app)


# SQL Alchemy
DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
    user="postgres", pw="mysecretpassword", url="192.168.99.100:5432", db="firefly")
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# entities
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(32), index=True)
    email = db.Column(db.String(50), index=True)
    password_hash = db.Column(db.String(128))
    created_date = db.Column(db.DateTime, nullable=False,
                             default=datetime.datetime.utcnow)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)


class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32), index=True)
    addresses = db.relationship(
        "CustomerAddress", uselist=False, backref=db.backref('customers'))
    created_date = db.Column(db.DateTime, nullable=False,
                             default=datetime.datetime.utcnow)


class CustomerAddress(db.Model):
    __tablename__ = 'customer_addresses'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey(
        'customers.id'), nullable=False)
    address = db.Column(db.String(128))

#reset db
@app.cli.command('resetdb')
def resetdb_command():
    """Destroys and creates the database + tables."""

    from sqlalchemy_utils import database_exists, create_database, drop_database
    if database_exists(DB_URL):
        print('Deleting database.')
        drop_database(DB_URL)
    if not database_exists(DB_URL):
        print('Creating database.')
        create_database(DB_URL)

    # db.drop_all()
    print('Creating tables.')
    db.create_all()
    print('Shiny!')


# api
# login methods
@api.route('/api/users/login')
@api.doc(params={'username': 'string'})
@api.doc(params={'password': 'string'})
class Login(Resource):
    def post(self):
        username, password = request.json.get(
            'username').strip(), request.json.get('password').strip()
        current_user = User.query.filter_by(username=username).first()
        if not current_user:
            return {'success': False, 'message': 'User {} doesn\'t exist'.format(username)}

        if current_user.verify_password(password):
            refresh_token = create_refresh_token(identity = username)
            access_token = create_access_token(identity =username)
            return {'access_token': str(access_token), 'refresh_token': str(refresh_token)}
        else:
            return {'success': False, 'message': 'Username or Password is wrong!'}


# register methods
@api.route('/api/users/register')
@api.doc(params={'username': 'username'})
@api.doc(params={'password': 'password'})
@api.doc(params={'email': 'email'})
class Register(Resource):
    def post(self):
        username, password, email = request.json.get('username').strip(
        ), request.json.get('password').strip(), request.json.get('email').strip()
        current_user = User.query.filter_by(username=username).first()
        if not current_user:
            new_user = User(username=username, email=email)
            new_user.password = new_user.hash_password(password)
            db.session.add(new_user)
            db.session.commit()
            return {"status": True, "message": "user created"}
        return {"status": False, "message": 'User {} exist'.format(username)}


@api.route("/api/customer/create")
class CreateCustomer(Resource):
    @jwt_required
    def post(self):
        pass


if __name__ == '__main__':
    app.run(debug=True)
