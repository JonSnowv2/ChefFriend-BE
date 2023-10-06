from flask import render_template
from config import app, db
from controllers import recipe_controller
import create_table

app.app_context().push()

with app.app_context():
    db.create_all()

recipes = recipe_controller.get_all_recipes()

@app.route('/')
def index():
    return render_template('index.html', recipes=recipes)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)