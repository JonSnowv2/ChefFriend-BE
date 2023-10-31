from datetime import timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databaseForAll.db'
app.config['JWT_SECRET_KEY'] = 'JonSnow&DragonIn#Westeros@Winterfell4Money'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=60)
jwt = JWTManager(app)

db = SQLAlchemy(app)

    

