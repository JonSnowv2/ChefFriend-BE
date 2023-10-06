from config import db

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    ingredients = db.Column(db.Text)
    instructions = db.Column(db.Text)
    category = db.Column(db.String(255))
    image = db.Column(db.String(255))

    def __init__(self, title, description, ingredients, instructions, category, image):
        self.title = title
        self.description = description
        self.ingredients = ingredients
        self.instructions = instructions
        self.category = category
        self.image = image

