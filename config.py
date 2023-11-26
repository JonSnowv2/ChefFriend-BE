from datetime import timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///westerosdatabase.db'
app.config['JWT_SECRET_KEY'] = 'JonSnow&DragonIn#Westeros@Winterfell4Money'
jwt = JWTManager(app)

db = SQLAlchemy(app)

    

