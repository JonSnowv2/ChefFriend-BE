# CHEF'S FRIEND
#### Video Demo:  <https://www.youtube.com/watch?v=x3ClvhyVKX4>
#### Description: Website where users can store their favorite recipes in detail, but also share their recipes with the world if they want to - the public recipes can be viewed by anyone using the site (so you can also use it to discover new recipes)

## Backend

The backend of the site is made using [Flask](https://flask.palletsprojects.com/en/3.0.x/), and the database is made using [SQLAlchemy](https://www.sqlalchemy.org/)

The **main.py** file is responsible for running the Flask App:

```
CORS(app, resources={r"/api/*": {"origins": "*"}})

if __name__ == '__main__':
    app.run(debug=True , host='0.0.0.0', port=8081)
```
<br>
[CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) is used to ensure proper connection and communication between with the Flutter Web Frontend.
<br>

The `config.py` file creates the Flask applcation and the SQLAlchemy database. <br>
The site uses token authentication so [Flask JWT](https://flask-jwt-extended.readthedocs.io/en/stable/) is used to verify the whether the user is authenticated or not, it is used to protect specific routes.

In the `authentication_service` folder there is one file - `authentication.py` - which handles user authentication. The `/register` and `/login` endpoints are found there. <br>
When registering, I use the **scrypt** library to hash the passwords when registration occurs. <br>
<br>

In the `models` directory are the two models, the two classes used - Recipe and User - with their constructor and type, like

```
id = db.Column(db.Integer, primary_key=True)
title = db.Column(db.String(255), nullable=False)
```
<br>
<br>

In the `service` folder you will find all the functions used to query data, edit data, delete data, and send data to the frontend. <br>
The `serialize_recipe.py` file ensures that the data of a Recipe object can be transmitted all at once without errors, by serializing the object. <br>
Finally, in the `recipe_service.py` and `user_service.py` you will be able to find what I've mentioned before, along with all the endpoints that can be reached by the frontend. All transmission of data is done using JSON files. <br>

In `recipe_service.py`, the code at the beginning, the method `protected_routes()` is a method that can be used inside any function you want to protect the endpoint from un-authorized users.

```
@jwt_required()
def protected_routes():
    user_username = get_jwt_identity()
    return user_username
```
<br>
<br>

## Be sure to check the repository with the frontend of this website - [Frontend](https://github.com/JonSnowv2/ChefFriend)!













