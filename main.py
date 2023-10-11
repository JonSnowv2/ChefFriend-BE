from config import app, db
from controllers import recipe_controller
from flask_cors import CORS
from authentication_service.authentication import register, login

CORS(app, resources={r"/api/*": {"origins": "*"}})

if __name__ == '__main__':
    app.run(debug=True , host='0.0.0.0', port=8081)
