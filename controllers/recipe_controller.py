from flask import current_app, jsonify
from config import db, app
from models.recipe import Recipe 

def create_recipe(title, description, ingredients, instructions, category, image):
    with current_app.app_context():
        new_recipe = Recipe(
            title=title,
            description=description,
            ingredients=ingredients,
            instructions=instructions,
            category=category,
            image=image
        )
        db.session.add(new_recipe)
        db.session.commit()

def get_all_recipes():
    return Recipe.query.all()

@app.route('/api/recipes', methods=['GET'])
def get_recipes():
    recipes = get_all_recipes()
    recipes_list = [
        {
            'title': recipe.title,
            'description': recipe.description,
            'ingredients': recipe.ingredients,
            'instructions': recipe.instructions,
            'category': recipe.category,
            'image': recipe.image
        }
        for recipe in recipes
    ]
    return jsonify(recipes_list)