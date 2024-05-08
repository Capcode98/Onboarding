from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)

socketIo = SocketIO(app, cors_allowed_origins="*")

from app import routes

