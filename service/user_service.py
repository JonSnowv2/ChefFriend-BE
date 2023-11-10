from flask import jsonify, request
from flask_cors import cross_origin
from config import db, app
from models.recipe import Recipe
from models.user import User
from passlib.hash import scrypt
from flask_sqlalchemy import SQLAlchemy

from service.serialize_recipe import serialize_recipe

def add_user(username, name, password):
    hashed_password = scrypt.hash(password)
    new_user = User(username=username, name=name, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

@app.route('/api/users', methods=['GET'])
@cross_origin(origin="*")
def get_all_users():
    users = User.query.all()
    
    user_list = []
    for user in users:
        user_data = {
            'username': user.username,
            'name': user.name,
            'password': user.password,
            'recipes': [recipe.id for recipe in user.recipes],
            'access_token': user.access_token,
            'favorites_list': [recipe.id for recipe in user.favorite_recipes],
        }
        user_list.append(user_data)
    
    return jsonify(user_list), 200

@app.route('/api/username_exists', methods=["GET", "POST"])
@cross_origin(origin="*")
def search_user_exist():
    username = request.form.get('username')

    user = User.query.filter_by(username=username).first()

    if user:
        response = {'exists': True}
    else:
        response = {'exists': False}

    return jsonify(response), 200

@app.route('/api/return_user', methods=['GET', 'POST'])
@cross_origin(origin="*")
def return_user():
    token_value = request.headers.get('Authorization')

    if token_value and token_value.startswith('Bearer '):
        token = token_value.split(' ')[1]

    print(token)

    if token:
        user = User.query.filter_by(access_token=token).first()

        if user:
            user_data = {
                'username': user.username,
                'name': user.username,
                'password': user.password,
                'recipes': [serialize_recipe(recipe) for recipe in user.recipes],
                'favorites_list': [recipe.id for recipe in user.favorite_recipes],
            }
            return jsonify({'user': user_data}), 200
        else:
            return jsonify({'message': 'User not found'}), 404
    else:
        return jsonify({'message': 'Token invalid or not provided'}), 400
    
@app.route('/api/return_user_recipes', methods=['POST', 'GET'])
@cross_origin(origin="*")
def return_user_and_recipes():
    data = request.get_json()

    if data is None:
        return jsonify({'error': 'Invalid JSON data in the request'}), 400

    username = data.get('username')

    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    user_data = {
        'recipes': [recipe.id for recipe in user.recipes],
    }

    print(user_data)

    return jsonify(user_data), 200

@app.route('/api/add_to_favorites', methods=['POST'])
@cross_origin(origin="*")
def add_to_favorites():
    data = request.get_json()

    if data is None:
        return jsonify({'error': 'Invalid JSON data in the request'}), 400
    
    token = data.get('token')
    recipe_id = data.get('recipeId')

    user = User.query.filter_by(access_token=token).first()

    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    recipe = Recipe.query.get(recipe_id)

    if not recipe:
        return jsonify({'message': 'Recipe not found'}), 404
    
    user.add_to_favorites(recipe)

    return jsonify({'message': 'Successfully added to favorites'}), 200

@app.route('/api/remove_from_favorites', methods=['POST'])
@cross_origin(origin="*")
def remove_from_recipes():
    data = request.get_json()

    if data is None:
        return jsonify({'error': 'Invalid JSON data in the request'}), 400
    
    token = data.get('token')
    recipe_id = data.get('recipeId')

    user = User.query.filter_by(access_token=token).first()

    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    recipe = Recipe.query.get(recipe_id)

    if not recipe:
        return jsonify({'message': 'Recipe not found'}), 404
    
    user.remove_from_favorites(recipe)

    return jsonify({'message': 'Successfully removed from favorites'}), 200

@app.route('/api/return_user_fav_recipes', methods=['POST', 'GET'])
@cross_origin("*")
def return_favorite_recipes():
    data = request.get_json()

    token = data['token']

    user = User.query.filter_by(access_token=token).first()

    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    favorite_recipes = user.favorite_recipes

    serialized_recipes = [serialize_recipe(recipe) for recipe in favorite_recipes]

    return jsonify({'favorite recipes': serialized_recipes}), 200




    
def print_schema():
    table = User.__table__
    for column in table.columns:
        print(f"Table: {table.name}, Column: {column.name}, Type: {column.type}")