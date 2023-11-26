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
    time_taken = data.get('time_taken')

    user_username = protected_routes()

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
            time_taken=time_taken,
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
            'time_taken': recipe.time_taken,
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
    
@app.route('/api/edit_recipe', methods=['POST'])
@cross_origin(origin="*")
def edit_recipe():
    try:
        data = request.json

        id = data.get('id')
        id = int(id)

        recipe = Recipe.query.filter_by(id=id).first()

        new_title = data.get('new_title')
        new_description = data.get('new_description')
        new_category = data.get('new_category')
        new_public = data.get('new_public')
        new_time_taken = data.get('new_time_taken')

        new_ingredients = data.get('new_ingredients')
        new_ingredients_list = ','.join(new_ingredients)

        new_instructions = data.get('new_instructions')
        new_instructions_list = ','.join(new_instructions)

        recipe.title = new_title
        recipe.description = new_description
        recipe.category = new_category
        recipe.public = new_public
        recipe.time_taken = new_time_taken
        recipe.ingredients = new_ingredients_list
        recipe.instructions = new_instructions_list

        db.session.commit()

        return jsonify({'message': 'successfull'}), 200
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': 'something went wrong'}), 400
        
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
            'time_taken': recipe.time_taken,
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
            'time_taken': recipe.time_taken,
        }
        for recipe in recipes
    ]

    return jsonify(recipes_list)

@app.route('/api/get_recipes_by_id', methods=['GET', 'POST'])
@cross_origin(origin='*')
def get_recipes_by_ids():
    data = request.get_json()

    if data is None:
        return jsonify({'error': 'Invalid JSON data in the request'}), 400

    list_ids = data.get('ids')

    if not list_ids:
        return jsonify({'message': 'No ids provided'}), 400

    recipes = Recipe.query.filter(Recipe.id.in_(list_ids), Recipe.public==1).all()

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
            'time_taken': recipe.time_taken,
        }
        for recipe in recipes
    ]

    return jsonify(recipes_list), 200

def print_schema():
    table = Recipe.__table__
    for column in table.columns:
        print(f"Table: {table.name}, Column: {column.name}, Type: {column.type}")





    