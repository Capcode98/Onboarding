from flask_jwt_extended import JWTManager
from app import app
import os

# Setup Flask-JWT-Extended
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET')  # Change this!
jwt = JWTManager(app)

