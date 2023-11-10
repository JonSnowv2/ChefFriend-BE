from config import db
from sqlalchemy.orm import relationship
from models.recipe import Recipe

favorites = db.Table(
    'favorites',
    db.Column('user_username', db.String, db.ForeignKey('user.username'), primary_key=True),
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'), primary_key=True)
)

class User(db.Model):
    username = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(20))
    password = db.Column(db.String(80))
    recipes = db.relationship('Recipe', backref='user', lazy=True)
    access_token = db.Column(db.String(255), nullable=True)

    favorite_recipes = db.relationship('Recipe', secondary=favorites, backref='favorited_by', lazy='dynamic')

    def __init__(self, username, name, password):
        self.username = username
        self.name = name
        self.password = password

    def add_to_favorites(self, recipe):
        if recipe not in self.favorite_recipes:
            self.favorite_recipes.append(recipe)
            db.session.commit()

    def remove_from_favorites(self, recipe):
        if recipe in self.favorite_recipes:
            self.favorite_recipes.remove(recipe)
            db.session.commit()

