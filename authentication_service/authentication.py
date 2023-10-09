from flask import g, jsonify, request
from flask_cors import cross_origin
from config import db, app
from models.user import User
from passlib.hash import scrypt
from controllers.user_controller import add_user

@app.route('/register', methods=['POST'])
@cross_origin(origin="*")
def register():
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        password = request.form['password']

        try:
            add_user(username, name, password)
            return jsonify({'message': 'User registered successfully'}), 200
        except Exception as e:
            return jsonify({'message': str(e)}), 500

@app.route('/login', methods=['GET', 'POST'])
@cross_origin(origin="*")
def login():
    if request.method == 'POST':
        data = request.get_json()

        if not data or 'username' not in data or 'password' not in data:
            return jsonify({'message': 'Invalid request'}), 400
        
        username = data['username']
        password = data['password']

        user = User.query.filter_by(username=username).first()

        if user:
            if scrypt.verify(password, user.password):
                user_data = {
                    'username': user.username,
                    'name': user.name,
                    'password': user.password,
                    'recipes': user.recipes
                }
                g.user = user
                print(g.user)
                return jsonify({'user': user_data}), 200
            return jsonify({'message': 'Invalid username or password'}), 401

    return jsonify({'message': 'Welcome to the login page'}), 200
