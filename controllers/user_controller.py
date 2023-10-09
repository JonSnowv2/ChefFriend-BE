from flask import jsonify
from flask_cors import cross_origin
from config import db, app
from models.user import User
from passlib.hash import scrypt

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
            'recipes': user.recipes,
        }
        user_list.append(user_data)
    
    return jsonify(user_list), 200