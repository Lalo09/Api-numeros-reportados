from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.sql import func

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username= db.Column(db.String(80),unique=True,nullable=False)
    email= db.Column(db.String(120),unique=True,nullable=False)
    password= db.Column(db.Text(),unique=True,nullable=False)
    created_at = db.Column(db.DateTime,default=datetime.now())
    updated_at = db.Column(db.DateTime,onupdate=datetime.now())
    number = db.relationship('Number',backref="user")

    def __repr__(self):
        return f'<User {self.username}>'
    
class Number(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(80),nullable=False)
    phone= db.Column(db.String(25),unique=True,nullable=False)
    account= db.Column(db.String(25))
    location= db.Column(db.String(100),nullable=False)
    reports = db.Column(db.Integer,default=1)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime,default=datetime.now())
    updated_at = db.Column(db.DateTime,onupdate=datetime.now())

def __repr__(self):
        return f'<Number {self.phone}>'
