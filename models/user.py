from config import db
from sqlalchemy.orm import relationship
from models.recipe import Recipe

class User(db.Model):
    username = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(20))
    password = db.Column(db.String(80))
    recipes = db.relationship('Recipe', backref='user', lazy=True)

    def __init__(self, username, name, password):
        self.username = username
        self.name = name
        self.password = password
