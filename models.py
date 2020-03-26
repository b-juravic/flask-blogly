"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """User Class"""
    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(30),
                           nullable=False)
    last_name = db.Column(db.String(30),
                          nullable=False)
    image_url = db.Column(db.String, default="https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Joseph_Ducreux_%28French%29_-_Self-Portrait%2C_Yawning_-_Google_Art_Project.jpg/1024px-Joseph_Ducreux_%28French%29_-_Self-Portrait%2C_Yawning_-_Google_Art_Project.jpg")
    posts = db.relationship('Post')


class Post(db.Model):
    """Post Class"""
    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(50),
                      nullable=False)
    content = db.Column(db.String,
                        nullable=False)
    created_at = db.Column(db.DateTime,
                           default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'))
    user = db.relationship('User')
