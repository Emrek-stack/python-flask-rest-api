import os
import datetime
from flask import Flask, request
from flask_restplus import Resource, Api
from flask_sqlalchemy import SQLAlchemy
#from api.account import HelloWorld

app = Flask(__name__)
api = Api(app)

# SQL Alchemyaoo
DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
    user="postgres", pw="mysecretpassword", url="192.168.99.100:5432", db="firefly")
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# entities


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(128))
    created_date = db.Column(db.DateTime, nullable=False,
                             default=datetime.datetime.utcnow)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)


class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32), index=True)
    addresses = db.relationship(
        'customer_address', backref='customer', lazy=True)
    created_date = db.Column(db.DateTime, nullable=False,
                             default=datetime.datetime.utcnow)


class CustomerAddress(db.Model):
    __tablename__ = 'customer_address'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey(
        'customer.id'), nullable=False)
    address = db.Column(db.String(128))


# def create_user
# @app.cli.command('resetdb')
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
# user methods
@api.route('/api/users')
class User(Resource):
    def post(self):
        username = request.json.get('username')
        password = request.json.get('password')
        return {username : username}
        # if username is None or password is None:
        #     abort(400)  # missing arguments
        # if User.query.filter_by(username=username).first() is not None:
        #     abort(400)  # existing user
        # user = User(username=username)
        # user.hash_password(password)
        # db.session.add(user)
        # db.session.commit()
        #return jsonify({'username': username}), 201, {'Location': url_for('get_user', id=username, _external=True)}


@api.route("/api/customer")
class Customer(Resource):
    def post(self):
        pass

if __name__ == '__main__':
    app.run(debug=True)
