from config import db
from sqlalchemy.orm import relationship

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255), nullable=True)
    public = db.Column(db.Integer, nullable=False)
    time_taken = db.Column(db.Integer, nullable=False)
    user_username = db.Column(db.String, db.ForeignKey('user.username'), nullable=False)

    def __init__(self, title, description, ingredients, instructions, category, image, user_username, public, time_taken):
        self.title = title
        self.description = description
        self.ingredients = ingredients
        self.instructions = instructions
        self.category = category
        self.image = image
        self.public = public
        self.user_username = user_username
        self.time_taken = time_taken
