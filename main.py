from flask import render_template
from config import app, db
from controllers import recipe_controller
from flask_cors import CORS

app.app_context().push()

with app.app_context():
    db.create_all()

CORS(app, resources={r"/api/*": {"origins": "*"}})

recipes = recipe_controller.get_all_recipes()

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True , host='0.0.0.0', port=8081)