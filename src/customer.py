from flask_sqlalchemy import SQLAlchemy
from app import db

class User(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(32), index = True)
    email = db.Column(db.String(32), index = True)
    password = db.Column(db.String(128))
    