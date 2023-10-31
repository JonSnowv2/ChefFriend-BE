from flask import current_app, jsonify, request, g
from flask_cors import cross_origin
from config import db, app
from models.recipe import Recipe 
from models.user import User
from authentication_service.authentication import login
from flask_jwt_extended import jwt_required, get_jwt_identity

@jwt_required()
def protected_routes():
    user_username = get_jwt_identity()
    return user_username


def get_all_recipes():
    return Recipe.query.all()

@app.route('/api/recipes/add', methods=['POST'])
@cross_origin(origin="*")
def create_recipe():
    data = request.json  
    title = data.get('title')
    description = data.get('description')
    ingredients_list = data.get('ingredients')
    instructions_list = data.get('instructions')
    category = data.get('category')
    image = data.get('image')
    public = data.get('public')

    user_username = protected_routes()

    if title is None or description is None or ingredients_list is None or instructions_list is None or category is None or image is None:
        return jsonify({'error': 'Missing required data in the request'}), 400

    ingredients = ','.join(ingredients_list)
    instructions = ','.join(instructions_list)

    with current_app.app_context():
        new_recipe = Recipe(
            title=title,
            description=description,
            ingredients=ingredients,
            instructions=instructions,
            category=category,
            image=image,
            public=public,
            user_username=user_username,
        )
        db.session.add(new_recipe)
        db.session.commit()

    return jsonify({'message': 'Recipe created successfully'}), 200

@app.route('/api/recipes', methods=['GET'])
@cross_origin(origin="*")
def get_recipes():
    user_username = protected_routes()
    
    recipes = Recipe.query.filter_by(user_username=user_username).all()

    recipes_list = [
        {
            'id': recipe.id,
            'title': recipe.title,
            'description': recipe.description,
            'ingredients': recipe.ingredients,
            'instructions': recipe.instructions,
            'category': recipe.category,
            'image': recipe.image,
            'public': recipe.public,
            'user_username': recipe.user_username,
        }
        for recipe in recipes
    ]
    return jsonify(recipes_list)


@app.route('/api/recipes/<int:recipe_id>', methods=['DELETE'])
@cross_origin(origin="*")
def delete_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    if recipe:
        db.session.delete(recipe)
        db.session.commit()
        return '', 204
    else:
        return jsonify({'error': 'Recipe not found'}), 404
    
@app.route('/api/get_all_recipes')
@cross_origin(origin="*")
def get_all_recipes():
    recipes = Recipe.query.all()
    recipes_list = [
        {
            'id': recipe.id,
            'title': recipe.title,
            'description': recipe.description,
            'ingredients': recipe.ingredients,
            'instructions': recipe.instructions,
            'category': recipe.category,
            'image': recipe.image,
            'user_username': recipe.user_username,
            'public': recipe.public,
        }
        for recipe in recipes
    ]
    return jsonify(recipes_list)

@app.route('/api/get_public_recipes', methods=['GET'])
@cross_origin(origin="*")
def return_public_recipes():
    recipes = Recipe.query.filter_by(public=1)
    recipes_list = [
        {
            'id': recipe.id,
            'title': recipe.title,
            'description': recipe.description,
            'ingredients': recipe.ingredients,
            'instructions': recipe.instructions,
            'category': recipe.category,
            'image': recipe.image,
            'user_username': recipe.user_username,
            'public': recipe.public,
        }
        for recipe in recipes
    ]

    return jsonify(recipes_list)

@app.route('/api/get_recipes_by_id', methods=['GET', 'POST'])
@cross_origin(origin='*')
def get_recipes_by_id():
    data = request.get_json()

    if data is None:
        return jsonify({'error': 'Invalid JSON data in the request'}), 400

    list_ids = data.get('ids')

    if not list_ids:
        return jsonify({'message': 'No ids provided'}), 400

    recipes = Recipe.query.filter(Recipe.id.in_(list_ids)).all()

    recipes_list = [
        {
            'id': recipe.id,
            'title': recipe.title,
            'description': recipe.description,
            'ingredients': recipe.ingredients,
            'instructions': recipe.instructions,
            'category': recipe.category,
            'image': recipe.image,
            'user_username': recipe.user_username,
            'public': recipe.public,
        }
        for recipe in recipes
    ]

    return jsonify(recipes_list), 200

def print_schema():
    table = Recipe.__table__
    for column in table.columns:
        print(f"Table: {table.name}, Column: {column.name}, Type: {column.type}")





    