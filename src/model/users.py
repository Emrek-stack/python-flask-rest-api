from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(32), index = True)
    password_hash = db.Column(db.String(128))
    userId = db.relationship('customer', backref='user', lazy=True)
    created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

   def __repr__(self):
       return '<User %r>' % self.username
       